#!/usr/bin/env python

import os
from pathlib import Path
import bodzify_api.settings as settings

ALLOWED_HOSTS = [
    '127.0.0.1'
]

STATICFILES_DIRS = [
    Path(settings.BASE_DIR) / 'static'
]
STATIC_ROOT =  Path(settings.BASE_DIR) / 'staticfiles'

MEDIA_ROOT = Path(settings.BASE_DIR) / 'media'