from django.contrib import admin
from .models import Resource, Review, Bookmark


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'file_type', 'uploaded_by', 'is_approved', 'created_at')
    list_filter = ('file_type', 'subject', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'subject', 'tags')
    list_editable = ('is_approved',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'subject', 'tags')
        }),
        ('File Information', {
            'fields': ('file_type', 'file_url')
        }),
        ('Status', {
            'fields': ('uploaded_by', 'is_approved')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('resource__title', 'user__username', 'comment')
    ordering = ('-created_at',)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'resource__title')
    ordering = ('-created_at',)
