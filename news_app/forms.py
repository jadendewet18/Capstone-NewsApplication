"""
Forms for the news_app application.

Provides Django ModelForms for user registration, articles, newsletters,
and publisher management.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article, CustomUser, Newsletter, Publisher


class CustomUserCreationForm(UserCreationForm):
    """Custom registration form exposing role selection for new users."""

    role = forms.ChoiceField(
        choices=CustomUser.Role.choices,
        required=True,
        label="Select Your Role",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta(UserCreationForm.Meta):
        """Meta options for CustomUserCreationForm."""

        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role')


class ArticleForm(forms.ModelForm):
    """Form for Journalists and Editors to create or update articles."""

    class Meta:
        """Meta options for ArticleForm."""

        model = Article
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
        }


class NewsletterForm(forms.ModelForm):
    """Form for Journalists and Editors to curate and manage newsletters."""

    class Meta:
        """Meta options for NewsletterForm."""

        model = Newsletter
        fields = ['title', 'description', 'articles']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'articles': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class PublisherForm(forms.ModelForm):
    """Form for creating and managing publishing organizations."""

    class Meta:
        """Meta options for PublisherForm."""

        model = Publisher
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }