#!/usr/bin/env python

import bodzify_api.settings as settings

ALLOWED_HOSTS = ['127.0.0.1']

STATIC_ROOT = settings.BASE_DIR / 'staticfiles'

MEDIA_ROOT = settings.BASE_DIR / 'media'

LOG_PATH = '/var/log/django/'
