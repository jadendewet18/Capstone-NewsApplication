"""
Django signals for article approval events.

Handles automated email dispatch to subscribers and triggers an internal HTTP
POST request to log approved articles to the API endpoint.
"""

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

from .models import Article


@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
    """
    Trigger notifications and external logging when an article is approved.

    Args:
        sender (Type[Article]): The Article model class.
        instance (Article): The specific Article instance being saved.
        created (bool): Indicates if the instance was newly created.
        **kwargs: Additional keyword arguments passed by post_save.
    """
    # Only act if the article is marked as approved
    if not instance.approved:
        return

    # 1. Collect subscribers (both journalist and publisher subscribers)
    subscribers = set()
    if instance.author:
        for reader in instance.author.journalist_subscribers.all():
            if reader.email:
                subscribers.add(reader.email)

    if instance.publisher:
        for reader in instance.publisher.reader_subscribers.all():
            if reader.email:
                subscribers.add(reader.email)

    # Send email notifications to subscribers
    if subscribers:
        send_mail(
            subject=f"New Approved Article: {instance.title}",
            message=(
                f"An article you subscribed to has been approved!\n\n"
                f"Title: {instance.title}\n"
                f"Author: {instance.author.username}\n\n"
                f"{instance.content}"
            ),
            from_email="noreply@newsapp.com",
            recipient_list=list(subscribers),
            fail_silently=True,
        )

    # 2. Simulate external API integration with a POST request to /api/approved/
    try:
        requests.post(
            "http://127.0.0.1:8000/api/approved/",
            json={
                "article_id": instance.id,
                "title": instance.title,
                "author": instance.author.username,
            },
            timeout=2,
        )
    except requests.exceptions.RequestException:
        # Prevent app crash if server isn't actively listening during manual testing
        pass