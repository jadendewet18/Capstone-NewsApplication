"""
App configuration for news_app.
"""

from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    """
    Configuration class for news_app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'

    def ready(self):
        """Import signals module on application startup."""
        import news_app.signals  # noqa: F401