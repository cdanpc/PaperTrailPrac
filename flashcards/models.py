from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Flashcard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_flashcards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class FlashcardItem(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='items')
    front_text = models.TextField()
    back_text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.flashcard.title} - Item {self.order}"


class StudySession(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='study_sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    items_studied = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.flashcard.title} ({self.correct_answers}/{self.items_studied})"
