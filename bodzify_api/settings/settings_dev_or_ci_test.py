#!/usr/bin/env python

from pathlib import Path

from bodzify_api.settings import settings

ALLOWED_HOSTS = ['127.0.0.1']
STATIC_ROOT = settings.BASE_DIR / 'staticfiles'
MEDIA_ROOT = settings.BASE_DIR / 'media'
LOG_PATH = Path('/var/log/django/')
JWT_AUTH = {
    'JWT_SECRET_KEY': 'new_secret_key',  # Change this to reset all tokens. For tests only.
}
CORS_ALLOW_ALL_ORIGINS = True
