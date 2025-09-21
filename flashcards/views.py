from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Flashcard, FlashcardItem, StudySession
from .forms import FlashcardForm, FlashcardItemForm, FlashcardSearchForm


def flashcard_list_view(request):
    """Browse all public flashcards"""
    form = FlashcardSearchForm(request.GET)
    flashcards = Flashcard.objects.filter(is_public=True).select_related('created_by')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        subject = form.cleaned_data.get('subject')
        
        if query:
            flashcards = flashcards.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(subject__icontains=query)
            )
        
        if subject:
            flashcards = flashcards.filter(subject__icontains=subject)
    
    paginator = Paginator(flashcards, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'flashcards': page_obj,
    }
    return render(request, 'flashcards/flashcard_list.html', context)


def flashcard_detail_view(request, pk):
    """View flashcard details"""
    flashcard = get_object_or_404(Flashcard, pk=pk)
    items = flashcard.items.all()
    
    # Get user's study sessions if logged in
    user_sessions = []
    if request.user.is_authenticated:
        user_sessions = StudySession.objects.filter(user=request.user, flashcard=flashcard).order_by('-completed_at')[:5]
    
    context = {
        'flashcard': flashcard,
        'items': items,
        'user_sessions': user_sessions,
    }
    return render(request, 'flashcards/flashcard_detail.html', context)


@login_required
def study_flashcard_view(request, pk):
    """Study flashcards"""
    flashcard = get_object_or_404(Flashcard, pk=pk)
    items = list(flashcard.items.all())
    
    if not items:
        messages.error(request, 'This flashcard set has no items yet.')
        return redirect('flashcards:flashcard_detail', pk=pk)
    
    if request.method == 'POST':
        # Process study session
        items_studied = len(items)
        correct_answers = 0
        
        for item in items:
            answer_key = f'item_{item.id}'
            user_answer = request.POST.get(answer_key, '').strip()
            # Simple comparison - in a real app, you might want more sophisticated matching
            if user_answer.lower() in item.back_text.lower() or item.back_text.lower() in user_answer.lower():
                correct_answers += 1
        
        # Save study session
        StudySession.objects.create(
            flashcard=flashcard,
            user=request.user,
            items_studied=items_studied,
            correct_answers=correct_answers
        )
        
        percentage = (correct_answers / items_studied) * 100
        messages.success(request, f'Study session completed! Score: {correct_answers}/{items_studied} ({percentage:.1f}%)')
        return redirect('flashcards:flashcard_detail', pk=pk)
    
    context = {
        'flashcard': flashcard,
        'items': items,
    }
    return render(request, 'flashcards/study_flashcard.html', context)


@login_required
def create_flashcard_view(request):
    """Create a new flashcard set"""
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.created_by = request.user
            flashcard.save()
            messages.success(request, 'Flashcard set created successfully! Now add items.')
            return redirect('flashcards:add_items', pk=flashcard.pk)
    else:
        form = FlashcardForm()
    
    return render(request, 'flashcards/create_flashcard.html', {'form': form})


@login_required
def add_items_view(request, pk):
    """Add items to a flashcard set"""
    flashcard = get_object_or_404(Flashcard, pk=pk)
    
    # Check if user owns this flashcard
    if flashcard.created_by != request.user:
        messages.error(request, 'You can only add items to your own flashcard sets.')
        return redirect('flashcards:flashcard_detail', pk=pk)
    
    if request.method == 'POST':
        form = FlashcardItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.flashcard = flashcard
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('flashcards:add_items', pk=pk)
    else:
        form = FlashcardItemForm()
    
    items = flashcard.items.all()
    
    context = {
        'flashcard': flashcard,
        'form': form,
        'items': items,
    }
    return render(request, 'flashcards/add_items.html', context)


@login_required
def my_flashcards_view(request):
    """View user's created flashcards"""
    flashcards = Flashcard.objects.filter(created_by=request.user).order_by('-created_at')
    
    paginator = Paginator(flashcards, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'flashcards': page_obj,
    }
    return render(request, 'flashcards/my_flashcards.html', context)
