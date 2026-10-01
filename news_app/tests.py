"""
Automated unit tests for the Capstone News Application API.

Tests user role access, subscription filtering, article creation,
editor approvals, and signals/notifications.
"""

from unittest.mock import patch

from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article, CustomUser, Newsletter, Publisher


class NewsAPITestCase(APITestCase):
    """
    Test suite for news API endpoints, permissions, and signals.
    """

    def setUp(self):
        """Set up test users, publishers, and initial articles."""
        # Create users for each role
        self.reader = CustomUser.objects.create_user(
            username="test_reader",
            password="password123",
            role=CustomUser.Role.READER,
            email="reader@example.com"
        )
        self.journalist = CustomUser.objects.create_user(
            username="test_journalist",
            password="password123",
            role=CustomUser.Role.JOURNALIST,
            email="journalist@example.com"
        )
        self.editor = CustomUser.objects.create_user(
            username="test_editor",
            password="password123",
            role=CustomUser.Role.EDITOR,
            email="editor@example.com"
        )

        # Create publisher
        self.publisher = Publisher.objects.create(
            name="Daily News",
            description="Leading news publication."
        )

        # Create approved and unapproved articles
        self.article_approved = Article.objects.create(
            title="Approved Article",
            content="Content for approved article.",
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )
        self.article_pending = Article.objects.create(
            title="Pending Article",
            content="Content for pending article.",
            author=self.journalist,
            publisher=self.publisher,
            approved=False
        )

    def test_list_approved_articles_public(self):
        """Verify unauthenticated users can view approved articles only."""
        url = reverse('article_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['title'],
            self.article_approved.title
        )

    def test_journalist_can_create_article(self):
        """Verify journalists can post new articles."""
        self.client.force_authenticate(user=self.journalist)
        url = reverse('article_list_create')
        data = {
            "title": "New Breaking News",
            "content": "Fresh breaking content."
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 3)

    def test_reader_cannot_create_article(self):
        """Verify readers are forbidden from posting articles."""
        self.client.force_authenticate(user=self.reader)
        url = reverse('article_list_create')
        data = {
            "title": "Unauthorized Article",
            "content": "Attempted reader content."
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribed_articles_endpoint(self):
        """Verify readers retrieve only content from subscribed authors/pubs."""
        # Subscribe reader to the journalist
        self.reader.subscribed_journalists.add(self.journalist)

        self.client.force_authenticate(user=self.reader)
        url = reverse('subscribed_articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch('requests.post')
    def test_article_approval_signal_and_email(self, mock_requests_post):
        """Verify signals fire email dispatch and API log on article approval."""
        # Add reader subscription to journalist
        self.reader.subscribed_journalists.add(self.journalist)

        # Approve pending article to trigger post_save signal
        self.article_pending.approved = True
        self.article_pending.save()

        # Check email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New Approved Article", mail.outbox[0].subject)

        # Check mock requests POST called
        self.assertTrue(mock_requests_post.called)