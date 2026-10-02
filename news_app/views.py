"""
Views for the news_app application.

Provides Django REST Framework API views for Articles, Subscriptions,
and Approved Logs, as well as template-rendering Web UI views for viewing
articles, managing user dashboards, subscriptions, publishers, newsletters,
and account registration.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ArticleForm, CustomUserCreationForm, NewsletterForm, PublisherForm
from .models import Article, CustomUser, Newsletter, Publisher
from .permissions import IsEditor, IsJournalistOrReadOnly
from .serializers import ArticleSerializer


# =============================================================================
# Custom Registration & Web UI Auth Views
# =============================================================================

def register_view(request):
    """
    Render and handle user registration.

    Allows new users to create an account, select their initial role,
    and automatically log in upon successful creation.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# =============================================================================
# Public Web UI Views
# =============================================================================

def home_view(request):
    """Render the homepage feed displaying all approved news articles."""
    approved_articles = Article.objects.filter(approved=True).order_by(
        '-created_at'
    )
    return render(request, 'news_app/index.html', {'articles': approved_articles})


def article_detail_view(request, pk):
    """Render detailed single-article view for approved news items."""
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'news_app/article_detail.html', {'article': article})


# =============================================================================
# Dashboard & Article Management
# =============================================================================

@login_required
def dashboard_view(request):
    """
    Render role-based dashboard for content submission and approval workflows.

    - Journalists view submitted articles and a creation form.
    - Editors view articles pending approval with options to approve or reject.
    - Readers receive general dashboard statistics and subscription links.
    """
    if request.method == 'POST':
        # Journalist Article Submission
        if request.user.role == CustomUser.Role.JOURNALIST:
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.approved = False
                article.save()
                messages.success(
                    request,
                    "Article submitted successfully! It is now pending Editor approval.",
                )
                return redirect('dashboard')

        # Editor Approval Action
        elif request.user.role == CustomUser.Role.EDITOR:
            article_id = request.POST.get('article_id')
            action = request.POST.get('action')

            if article_id:
                article = get_object_or_404(Article, id=article_id)
                if action == 'approve':
                    article.approved = True
                    article.save()
                    messages.success(
                        request,
                        f"Article '{article.title}' has been approved and published!",
                    )
                elif action == 'reject':
                    article.delete()
                    messages.info(request, "Article draft rejected and removed.")
                return redirect('dashboard')

    form = ArticleForm()
    publishers = Publisher.objects.all()
    context = {'form': form, 'publishers': publishers}

    if request.user.role == CustomUser.Role.JOURNALIST:
        context['my_articles'] = Article.objects.filter(
            author=request.user
        ).order_by('-created_at')

    elif request.user.role == CustomUser.Role.EDITOR:
        context['pending_articles'] = Article.objects.filter(
            approved=False
        ).order_by('-created_at')

    return render(request, 'news_app/dashboard.html', context)


@login_required
def article_edit_view(request, pk):
    """Allow journalists or editors to edit existing articles."""
    article = get_object_or_404(Article, pk=pk)

    # Permission check: Author or Editor only
    if request.user != article.author and not request.user.is_editor():
        messages.error(request, "You do not have permission to edit this article.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f"Article '{article.title}' updated successfully!")
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'news_app/article_form.html', {'form': form, 'article': article})


@login_required
def article_delete_view(request, pk):
    """Allow journalists or editors to delete articles."""
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author and not request.user.is_editor():
        messages.error(request, "You do not have permission to delete this article.")
        return redirect('dashboard')

    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f"Article '{title}' deleted successfully.")
        return redirect('dashboard')

    return render(request, 'news_app/article_confirm_delete.html', {'article': article})


# =============================================================================
# Newsletter Views (CRUD)
# =============================================================================

def newsletter_list_view(request):
    """Public view: List all available newsletters with article previews."""
    newsletters = Newsletter.objects.all().order_by('-created_at')
    return render(request, 'news_app/newsletter_list.html', {'newsletters': newsletters})


@login_required
def newsletter_detail_view(request, pk):
    """Protected view: Full newsletter content and attached articles (Members Only)."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'news_app/newsletter_detail.html', {'newsletter': newsletter})


@login_required
def newsletter_create_view(request):
    """Allow Journalists and Editors to create new newsletters."""
    if not (request.user.is_journalist() or request.user.is_editor()):
        messages.error(request, "Only Journalists and Editors can create newsletters.")
        return redirect('newsletter_list')

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            messages.success(request, "Newsletter published successfully!")
            return redirect('newsletter_list')
    else:
        form = NewsletterForm()

    return render(request, 'news_app/newsletter_form.html', {'form': form, 'title': 'Create Newsletter'})


@login_required
def newsletter_edit_view(request, pk):
    """Allow Journalists or Editors to edit an existing newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.user != newsletter.author and not request.user.is_editor():
        messages.error(request, "You do not have permission to edit this newsletter.")
        return redirect('newsletter_list')

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully!")
            return redirect('newsletter_detail', pk=newsletter.pk)
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, 'news_app/newsletter_form.html', {'form': form, 'title': 'Edit Newsletter'})


@login_required
def newsletter_delete_view(request, pk):
    """Allow Journalists or Editors to delete a newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.user != newsletter.author and not request.user.is_editor():
        messages.error(request, "You do not have permission to delete this newsletter.")
        return redirect('newsletter_list')

    if request.method == 'POST':
        title = newsletter.title
        newsletter.delete()
        messages.success(request, f"Newsletter '{title}' deleted successfully.")
        return redirect('newsletter_list')

    return render(request, 'news_app/newsletter_confirm_delete.html', {'newsletter': newsletter})


# =============================================================================
# Publisher & Subscription Views
# =============================================================================

def publisher_list_view(request):
    """List all publishers and provide subscribe/unsubscribe actions."""
    publishers = Publisher.objects.all()
    journalists = CustomUser.objects.filter(role=CustomUser.Role.JOURNALIST)
    return render(
        request,
        'news_app/publisher_list.html',
        {'publishers': publishers, 'journalists': journalists},
    )


@login_required
def publisher_create_view(request):
    """Allow Editors to create new publishing organizations."""
    if not request.user.is_editor():
        messages.error(request, "Only Editors can manage publishers.")
        return redirect('publisher_list')

    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Publisher created successfully!")
            return redirect('publisher_list')
    else:
        form = PublisherForm()

    return render(request, 'news_app/publisher_form.html', {'form': form})


@login_required
def toggle_publisher_subscription_view(request, pk):
    """Toggle subscription status for a Publisher."""
    publisher = get_object_or_404(Publisher, pk=pk)
    user = request.user

    if publisher in user.subscribed_publishers.all():
        user.subscribed_publishers.remove(publisher)
        messages.info(request, f"Unsubscribed from {publisher.name}.")
    else:
        user.subscribed_publishers.add(publisher)
        messages.success(request, f"Subscribed to {publisher.name}!")

    return redirect('publisher_list')


@login_required
def toggle_journalist_subscription_view(request, pk):
    """Toggle subscription status for a Journalist."""
    journalist = get_object_or_404(CustomUser, pk=pk, role=CustomUser.Role.JOURNALIST)
    user = request.user

    if journalist in user.subscribed_journalists.all():
        user.subscribed_journalists.remove(journalist)
        messages.info(request, f"Unsubscribed from Journalist {journalist.username}.")
    else:
        user.subscribed_journalists.add(journalist)
        messages.success(request, f"Subscribed to Journalist {journalist.username}!")

    return redirect('publisher_list')


# =============================================================================
# REST API Endpoints
# =============================================================================

class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint to list all approved articles or create a new article."""

    serializer_class = ArticleSerializer
    permission_classes = [IsJournalistOrReadOnly]

    def get_queryset(self):
        return Article.objects.filter(approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribedArticlesAPIView(generics.ListAPIView):
    """API endpoint listing articles from publishers subscribed to by the user."""

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        subscribed_publishers = self.request.user.subscribed_publishers.all()
        return Article.objects.filter(
            publisher__in=subscribed_publishers, approved=True
        ).order_by('-created_at')


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint to retrieve, update, or delete a specific article instance."""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsJournalistOrReadOnly]


class ApprovedArticleLogAPIView(APIView):
    """API endpoint logging and returning all approved articles for Editors."""

    permission_classes = [permissions.IsAuthenticated, IsEditor]

    def get(self, request):
        approved_articles = Article.objects.filter(approved=True).order_by(
            '-created_at'
        )
        serializer = ArticleSerializer(approved_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)