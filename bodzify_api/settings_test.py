#!/usr/bin/env python

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://bodzify.com']


ALLOWED_HOSTS = [
    'bodzify.com',
    'www.bodzify.com',
]

STATICFILES_DIRS = [
    "/home/app/webapp/static/",
]
STATIC_ROOT =  "/home/app/webapp/staticfiles/"

MEDIA_ROOT = "/var/lib/bodzify-api/media/"
