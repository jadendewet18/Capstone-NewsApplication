"""
Admin configuration for news_app models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Article, CustomUser, Newsletter, Publisher


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom admin interface for managing CustomUser accounts and roles."""

    # Displays role directly in the main user table list
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

    # Adds role selection field to both creation and edit forms
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Roles', {'fields': ('role',)}),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for news articles."""

    list_display = ('title', 'author', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('title', 'content')


admin.site.register(Publisher)
admin.site.register(Newsletter)