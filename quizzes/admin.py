from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizAttempt


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'is_public', 'created_at')
    list_filter = ('subject', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'subject')
    inlines = [QuizQuestionInline]
    ordering = ('-created_at',)


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question', 'correct_answer')
    list_filter = ('quiz__subject', 'correct_answer')
    search_fields = ('question', 'quiz__title')
    ordering = ('quiz', 'id')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score', 'total_questions', 'completed_at')
    list_filter = ('completed_at', 'quiz__subject')
    search_fields = ('quiz__title', 'user__username')
    ordering = ('-completed_at',)
