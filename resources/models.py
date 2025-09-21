from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Resource(models.Model):
    TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('ppt', 'PowerPoint'),
        ('docx', 'Word Document'),
        ('ebook', 'E-book'),
        ('quiz', 'Quiz'),
        ('flashcard', 'Flashcard'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    tags = models.CharField(max_length=500, help_text="Comma-separated tags")
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file_url = models.URLField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Review(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['resource', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.resource.title} ({self.rating} stars)"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"
