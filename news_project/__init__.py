from django.db.backends.base.base import BaseDatabaseWrapper

# Bypass Django version check for MySQL 8.0.x
BaseDatabaseWrapper.check_database_version_supported = lambda self: None