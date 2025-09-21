from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from .models import Resource, Review, Bookmark
from .forms import ResourceForm, ReviewForm, ResourceSearchForm


def resource_list_view(request):
    """Browse all resources with search and filter"""
    form = ResourceSearchForm(request.GET)
    resources = Resource.objects.filter(is_approved=True).select_related('uploaded_by')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        subject = form.cleaned_data.get('subject')
        file_type = form.cleaned_data.get('file_type')
        
        if query:
            resources = resources.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(tags__icontains=query)
            )
        
        if subject:
            resources = resources.filter(subject__icontains=subject)
        
        if file_type:
            resources = resources.filter(file_type=file_type)
    
    # Add average rating to each resource
    for resource in resources:
        avg_rating = resource.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        resource.avg_rating = avg_rating if avg_rating is not None else 0
    
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'resources': page_obj,
    }
    return render(request, 'resources/resource_list.html', context)


def resource_detail_view(request, pk):
    """View resource details with reviews"""
    resource = get_object_or_404(Resource, pk=pk)
    reviews = resource.reviews.select_related('user').order_by('-created_at')
    
    # Check if user has bookmarked this resource
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, resource=resource).exists()
    
    # Check if user has reviewed this resource
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(user=request.user, resource=resource)
        except Review.DoesNotExist:
            pass
    
    # Calculate average rating
    avg_rating = resource.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    if avg_rating is None:
        avg_rating = 0
    
    context = {
        'resource': resource,
        'reviews': reviews,
        'is_bookmarked': is_bookmarked,
        'user_review': user_review,
        'avg_rating': avg_rating,
    }
    return render(request, 'resources/resource_detail.html', context)


@login_required
def upload_resource_view(request):
    """Upload new resource"""
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, 'Resource uploaded successfully! It will be reviewed before being published.')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    
    return render(request, 'resources/upload_resource.html', {'form': form})


@login_required
def add_review_view(request, pk):
    """Add or update review for a resource"""
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.get_or_create(
                user=request.user,
                resource=resource,
                defaults=form.cleaned_data
            )
            if not created:
                review.rating = form.cleaned_data['rating']
                review.comment = form.cleaned_data['comment']
                review.save()
            
            messages.success(request, 'Review submitted successfully!')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        # Try to get existing review
        try:
            existing_review = Review.objects.get(user=request.user, resource=resource)
            form = ReviewForm(instance=existing_review)
        except Review.DoesNotExist:
            form = ReviewForm()
    
    return render(request, 'resources/add_review.html', {
        'form': form,
        'resource': resource
    })


@login_required
def bookmark_resource_view(request, pk):
    """Bookmark or remove bookmark for a resource"""
    resource = get_object_or_404(Resource, pk=pk)
    
    try:
        bookmark = Bookmark.objects.get(user=request.user, resource=resource)
        bookmark.delete()
        messages.success(request, 'Resource removed from bookmarks.')
    except Bookmark.DoesNotExist:
        Bookmark.objects.create(user=request.user, resource=resource)
        messages.success(request, 'Resource added to bookmarks.')
    
    return redirect('resources:resource_detail', pk=resource.pk)


@login_required
def my_bookmarks_view(request):
    """View user's bookmarked resources"""
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('resource').order_by('-created_at')
    
    paginator = Paginator(bookmarks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'bookmarks': page_obj,
    }
    return render(request, 'resources/my_bookmarks.html', context)
