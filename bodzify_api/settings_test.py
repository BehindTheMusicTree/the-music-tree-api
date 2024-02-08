#!/usr/bin/env python

from pathlib import Path


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://bodzify.com']


ALLOWED_HOSTS = [
    'bodzify.com',
    'www.bodzify.com',
]

STATICFILES_DIRS = [
    Path('/home/app/webapp/static/'),
]
STATIC_ROOT =  Path('/home/app/webapp/staticfiles/')

MEDIA_ROOT = Path('/var/lib/bodzify-api/media/')
