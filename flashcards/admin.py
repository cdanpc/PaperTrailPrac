from django.contrib import admin
from .models import Flashcard, FlashcardItem, StudySession


class FlashcardItemInline(admin.TabularInline):
    model = FlashcardItem
    extra = 1


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'is_public', 'created_at')
    list_filter = ('subject', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'subject')
    inlines = [FlashcardItemInline]
    ordering = ('-created_at',)


@admin.register(FlashcardItem)
class FlashcardItemAdmin(admin.ModelAdmin):
    list_display = ('flashcard', 'front_text', 'order')
    list_filter = ('flashcard__subject',)
    search_fields = ('front_text', 'back_text', 'flashcard__title')
    ordering = ('flashcard', 'order')


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('flashcard', 'user', 'correct_answers', 'items_studied', 'completed_at')
    list_filter = ('completed_at', 'flashcard__subject')
    search_fields = ('flashcard__title', 'user__username')
    ordering = ('-completed_at',)
