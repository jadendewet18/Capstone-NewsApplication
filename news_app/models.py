"""
Database models for the Capstone News Application.

Includes custom user accounts with role-based access, publishers,
articles, and curated newsletters.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model supporting Reader, Editor, and Journalist roles.

    Attributes:
        role (str): Role designation for access control.
        subscribed_publishers (QuerySet): Publishers subscribed to by Reader.
        subscribed_journalists (QuerySet): Journalists subscribed to by Reader.
    """

    class Role(models.TextChoices):
        READER = 'READER', 'Reader'
        EDITOR = 'EDITOR', 'Editor'
        JOURNALIST = 'JOURNALIST', 'Journalist'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
        help_text='Designates the role and access permissions for this user.'
    )

    # Reader-specific subscription fields
    subscribed_publishers = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='reader_subscribers',
        help_text='Publishers subscribed to by this reader.'
    )
    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='journalist_subscribers',
        help_text='Journalists subscribed to by this reader.'
    )

    def is_reader(self):
        """Check if user has Reader role."""
        return self.role == self.Role.READER

    def is_editor(self):
        """Check if user has Editor role."""
        return self.role == self.Role.EDITOR

    def is_journalist(self):
        """Check if user has Journalist role."""
        return self.role == self.Role.JOURNALIST


class Publisher(models.Model):
    """
    Represents a news publishing organization.

    Attributes:
        name (str): Name of the publisher.
        description (str): Detailed overview of the publisher.
        editors (QuerySet): Editors managing this publication.
        journalists (QuerySet): Journalists writing for this publication.
        created_at (datetime): Timestamp when publisher was created.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='editing_publishers'
    )
    journalists = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='journalism_publishers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return human-readable publisher representation."""
        return self.name


class Article(models.Model):
    """
    Represents an individual news article.

    Attributes:
        title (str): Article title.
        content (str): Full text content of the article.
        author (CustomUser): Journalist who authored the article.
        publisher (Publisher): Optional associated publisher.
        approved (bool): Approval status set by an editor.
        created_at (datetime): Timestamp of creation.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    approved = models.BooleanField(
        default=False,
        help_text='Designates whether an editor has approved this article.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return human-readable article representation."""
        return self.title


class Newsletter(models.Model):
    """
    Curated collection of news articles created by journalists or editors.

    Attributes:
        title (str): Title of the newsletter issue.
        description (str): Overview of newsletter topics.
        author (CustomUser): User who curated the newsletter.
        articles (QuerySet): Articles included in this newsletter.
        created_at (datetime): Timestamp of creation.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )
    articles = models.ManyToManyField(
        Article,
        related_name='newsletters'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return human-readable newsletter representation."""
        return self.title