"""
Custom permission classes for news_app API endpoints.
"""

from rest_framework import permissions
from .models import CustomUser


class IsJournalistOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone,
    but restrict creation/editing to users with the Journalist role.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == CustomUser.Role.JOURNALIST
        )


class IsEditor(permissions.BasePermission):
    """
    Custom permission to restrict access exclusively to users with the Editor role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == CustomUser.Role.EDITOR
        )