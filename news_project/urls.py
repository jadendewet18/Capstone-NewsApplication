"""
Main URL configuration for news_project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Custom auth routes
    path('', include('news_app.urls')),
]