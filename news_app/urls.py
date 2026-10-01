"""
URL patterns for news_app REST API endpoints and template views.
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ApprovedArticleLogAPIView,
    ArticleDetailAPIView,
    ArticleListCreateAPIView,
    SubscribedArticlesAPIView,
    article_delete_view,
    article_detail_view,
    article_edit_view,
    dashboard_view,
    home_view,
    newsletter_create_view,
    newsletter_delete_view,
    newsletter_detail_view,
    newsletter_edit_view,
    newsletter_list_view,
    publisher_create_view,
    publisher_list_view,
    register_view,
    toggle_journalist_subscription_view,
    toggle_publisher_subscription_view,
)

urlpatterns = [
    # Web UI Core & Articles
    path('', home_view, name='home'),
    path('article/<int:pk>/', article_detail_view, name='article_detail'),
    path('article/<int:pk>/edit/', article_edit_view, name='article_edit'),
    path('article/<int:pk>/delete/', article_delete_view, name='article_delete'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register/', register_view, name='register'),

    # Web UI Newsletters
    path('newsletters/', newsletter_list_view, name='newsletter_list'),
    path('newsletters/create/', newsletter_create_view, name='newsletter_create'),
    path('newsletters/<int:pk>/', newsletter_detail_view, name='newsletter_detail'),
    path('newsletters/<int:pk>/edit/', newsletter_edit_view, name='newsletter_edit'),
    path('newsletters/<int:pk>/delete/', newsletter_delete_view, name='newsletter_delete'),

    # Web UI Publishers & Subscriptions
    path('publishers/', publisher_list_view, name='publisher_list'),
    path('publishers/create/', publisher_create_view, name='publisher_create'),
    path(
        'publishers/<int:pk>/subscribe/',
        toggle_publisher_subscription_view,
        name='toggle_publisher_subscription',
    ),
    path(
        'journalists/<int:pk>/subscribe/',
        toggle_journalist_subscription_view,
        name='toggle_journalist_subscription',
    ),

    # REST API Routes
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path(
        'api/articles/',
        ArticleListCreateAPIView.as_view(),
        name='article_list_create',
    ),
    path(
        'api/articles/subscribed/',
        SubscribedArticlesAPIView.as_view(),
        name='subscribed_articles',
    ),
    path(
        'api/articles/<int:pk>/',
        ArticleDetailAPIView.as_view(),
        name='article_detail_api',
    ),
    path(
        'api/approved/',
        ApprovedArticleLogAPIView.as_view(),
        name='approved_article_log',
    ),
]