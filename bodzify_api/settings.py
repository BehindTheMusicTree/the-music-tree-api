#!/usr/bin/env python

"""
For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import pathlib
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Before calling a view function, Django starts a transaction. 
# If the response is produced without problems, Django commits the transaction. 
# If the view produces an exception, Django rolls back the transaction.
ATOMIC_REQUESTS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'drf_spectacular',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'coverage',
    'drf_multiple_model',
    'bodzify_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bodzify_api.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_DATABASE'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'DISABLE_SERVER_SIDE_CURSORS': True
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bodzify_api.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': 'v1'
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'bodzify API',
    'DESCRIPTION': 'API to handle genre oriented music libraries',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

LOG_PATH = "/var/log/bodzify-api/"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]- %(message)s'}

    },
    'handlers': {
        'general': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'general.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'info': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'info.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'access': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'access.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['general', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'info': {
            'handlers': ['info'],
            'level': 'DEBUG',
            'propagate': True
        },
        'gunicorn.access' : { 
                'handlers': ['access'], 
                'level': 'DEBUG', 
                'propagate': True
        }
    },
}

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']

API_ROOT_BASE = 'api/v1/'
APP_NAME = "bodzify_api"
APP_ROOT = os.path.join(BASE_DIR, APP_NAME + '/')
MEDIA_ROOT = "/var/lib/bodzify-api/media/"
MEDIA_TEMP = os.path.join(MEDIA_ROOT, "temp/")
LIBRARIES_DIR_NAME = "libraries"
LIBRARIES_PATH = os.path.join(MEDIA_ROOT, LIBRARIES_DIR_NAME + '/')
USER_LIBRARY_DIR_NAME_PREFIXE = "user_"
TRACK_FILE_SIZE_MIN_IN_MO = 0
TRACK_FILE_SIZE_MAX_IN_MO = 500
TRACK_FILE_CONTENT_TYPES = ['audio/mpeg', 'audio/flac', 'audio/wav']
TRACK_FILENAME_MAX_CHAR = 100
TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LEN = 20
TRACK_TITLE_MAX_CHAR = 100
TRACK_GENERATED_TITLE_LEN = 20
TRACK_GENERATED_TITLE_PREFIXE = "bodzify_"
TRACK_RATING_MAX_VALUE = 10
TRACK_LANGUAGE_MAX_CHAR = 100
MINE_TRACK_TITLE_MAX_CHAR = 200
MINE_TRACK_RELEASED_ON_MAX_CHAR = 200
MINE_TRACK_URL_MAX_CHAR = 1000
ALBUM_NAME_MAX_CHAR = 100
ALBUM_ARTISTS_FIELD_MAX_CHAR = 100
ARTIST_NAME_MAX_CHAR = 100
CRITERIA_NAME_MAX_CHAR = 50
PLAYLIST_NAME_MAX_CHAR = 50

PAGINATION_LIMIT_OFFSET_DEFAULT = 30

ALLOWED_HOSTS = [
    'bodzify.com',
    'www.bodzify.com',
    '85.31.236.153'
]

if os.getenv('ENV') == 'DEV':
    from bodzify_api.settings_dev import *
elif os.getenv('ENV') == 'TEST':
    from bodzify_api.settings_test import *
