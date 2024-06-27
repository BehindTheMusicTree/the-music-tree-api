#!/usr/bin/env python

from pathlib import Path


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://bodzify.com']
ALLOWED_HOSTS = [
    'bodzify.com',
    'www.bodzify.com',
]
CORS_ALLOWED_ORIGINS = []
