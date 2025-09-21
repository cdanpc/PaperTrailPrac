from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Q
from resources.models import Resource, Review, Bookmark
from quizzes.models import Quiz
from flashcards.models import Flashcard
from accounts.models import User


def home_view(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')


@login_required
def dashboard_view(request):
    """User dashboard"""
    user = request.user
    
    # Get user's recent uploads (with error handling)
    try:
        recent_uploads = Resource.objects.filter(uploaded_by=user).order_by('-created_at')[:5]
    except:
        recent_uploads = []
    
    # Get user's bookmarks (with error handling)
    try:
        user_bookmarks = Bookmark.objects.filter(user=user).select_related('resource')[:5]
    except:
        user_bookmarks = []
    
    # Get user's reviews (with error handling)
    try:
        user_reviews = Review.objects.filter(user=user).select_related('resource')[:5]
    except:
        user_reviews = []
    
    # Get user's quizzes (with error handling)
    try:
        user_quizzes = Quiz.objects.filter(created_by=user).order_by('-created_at')[:5]
    except:
        user_quizzes = []
    
    # Get user's flashcards (with error handling)
    try:
        user_flashcards = Flashcard.objects.filter(created_by=user).order_by('-created_at')[:5]
    except:
        user_flashcards = []
    
    context = {
        'recent_uploads': recent_uploads,
        'user_bookmarks': user_bookmarks,
        'user_reviews': user_reviews,
        'user_quizzes': user_quizzes,
        'user_flashcards': user_flashcards,
    }
    
    return render(request, 'core/dashboard.html', context)


@staff_member_required
def admin_dashboard_view(request):
    """Admin dashboard"""
    # Get statistics
    total_users = User.objects.count()
    total_resources = Resource.objects.count()
    total_reviews = Review.objects.count()
    total_quizzes = Quiz.objects.count()
    total_flashcards = Flashcard.objects.count()
    
    # Get recent activity
    recent_resources = Resource.objects.select_related('uploaded_by').order_by('-created_at')[:10]
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get top subjects
    top_subjects = Resource.objects.values('subject').annotate(
        count=Count('subject')
    ).order_by('-count')[:10]
    
    context = {
        'total_users': total_users,
        'total_resources': total_resources,
        'total_reviews': total_reviews,
        'total_quizzes': total_quizzes,
        'total_flashcards': total_flashcards,
        'recent_resources': recent_resources,
        'recent_users': recent_users,
        'top_subjects': top_subjects,
    }
    
    return render(request, 'core/admin_dashboard.html', context)
