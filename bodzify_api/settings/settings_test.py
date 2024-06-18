#!/usr/bin/env python

from pathlib import Path


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://bodzify.com']
ALLOWED_HOSTS = [
    'bodzify.com',
    'www.bodzify.com',
]
STATIC_ROOT = Path('/home/app/webapp/staticfiles/')
MEDIA_ROOT = Path('/home/app/webapp/lib/bodzify-api/media/')
LOG_PATH = Path('/home/app/webapp/log/django/')
CORS_ALLOWED_ORIGINS = []
FILE_UPLOAD_TEMP_DIR = '/tmp/bodzify-api/uploaded-files/'
