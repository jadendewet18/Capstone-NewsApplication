"""
Serializers for the Capstone News Application API.

Handles serialization and deserialization of users, publishers,
articles, and newsletters with proper validation and field exposure.
"""

from rest_framework import serializers
from .models import Article, CustomUser, Newsletter, Publisher


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser instances.

    Exposes public user information and subscription fields.
    """

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'role',
            'subscribed_publishers',
            'subscribed_journalists',
        ]
        read_only_fields = ['id']


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for Publisher instances.
    """

    class Meta:
        model = Publisher
        fields = [
            'id',
            'name',
            'description',
            'editors',
            'journalists',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article instances.
    """

    author_username = serializers.ReadOnlyField(source='author.username')
    publisher_name = serializers.ReadOnlyField(source='publisher.name')

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'author_username',
            'publisher',
            'publisher_name',
            'approved',
            'created_at',
        ]
        read_only_fields = ['id', 'author', 'approved', 'created_at']


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for Newsletter instances.
    """

    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Newsletter
        fields = [
            'id',
            'title',
            'description',
            'author',
            'author_username',
            'articles',
            'created_at',
        ]
        read_only_fields = ['id', 'author', 'created_at']