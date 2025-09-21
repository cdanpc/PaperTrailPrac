from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Quiz, QuizQuestion, QuizAttempt
from .forms import QuizForm, QuizQuestionForm, QuizSearchForm


def quiz_list_view(request):
    """Browse all public quizzes"""
    form = QuizSearchForm(request.GET)
    quizzes = Quiz.objects.filter(is_public=True).select_related('created_by')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        subject = form.cleaned_data.get('subject')
        
        if query:
            quizzes = quizzes.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(subject__icontains=query)
            )
        
        if subject:
            quizzes = quizzes.filter(subject__icontains=subject)
    
    paginator = Paginator(quizzes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'quizzes': page_obj,
    }
    return render(request, 'quizzes/quiz_list.html', context)


def quiz_detail_view(request, pk):
    """View quiz details"""
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    
    # Get user's attempts if logged in
    user_attempts = []
    if request.user.is_authenticated:
        user_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-completed_at')[:5]
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'user_attempts': user_attempts,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def take_quiz_view(request, pk):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    
    if not questions.exists():
        messages.error(request, 'This quiz has no questions yet.')
        return redirect('quizzes:quiz_detail', pk=pk)
    
    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        
        for question in questions:
            answer_key = f'question_{question.id}'
            user_answer = request.POST.get(answer_key)
            if user_answer == question.correct_answer:
                score += 1
        
        # Save attempt
        QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            total_questions=total_questions
        )
        
        percentage = (score / total_questions) * 100
        messages.success(request, f'Quiz completed! Score: {score}/{total_questions} ({percentage:.1f}%)')
        return redirect('quizzes:quiz_detail', pk=pk)
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/take_quiz.html', context)


@login_required
def create_quiz_view(request):
    """Create a new quiz"""
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            messages.success(request, 'Quiz created successfully! Now add questions.')
            return redirect('quizzes:add_questions', pk=quiz.pk)
    else:
        form = QuizForm()
    
    return render(request, 'quizzes/create_quiz.html', {'form': form})


@login_required
def add_questions_view(request, pk):
    """Add questions to a quiz"""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    # Check if user owns this quiz
    if quiz.created_by != request.user:
        messages.error(request, 'You can only add questions to your own quizzes.')
        return redirect('quizzes:quiz_detail', pk=pk)
    
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('quizzes:add_questions', pk=pk)
    else:
        form = QuizQuestionForm()
    
    questions = quiz.questions.all()
    
    context = {
        'quiz': quiz,
        'form': form,
        'questions': questions,
    }
    return render(request, 'quizzes/add_questions.html', context)


@login_required
def my_quizzes_view(request):
    """View user's created quizzes"""
    quizzes = Quiz.objects.filter(created_by=request.user).order_by('-created_at')
    
    paginator = Paginator(quizzes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'quizzes': page_obj,
    }
    return render(request, 'quizzes/my_quizzes.html', context)
