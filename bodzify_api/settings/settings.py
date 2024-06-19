#!/usr/bin/env python

import psycopg2
import hashlib
import datetime
import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()


class ENV_VALUES:
    DEV = 'DEV'
    CI_TEST = 'CI_TEST'
    BUILD = 'BUILD'
    TEST = 'TEST'
    PROD = 'PROD'


ENV = os.getenv('ENV')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

API_VERSION = 'v1'
API_NAME = "bodzify_api"
API_DESCRIPTION = "API to handle genre oriented music libraries"
API_ROOT_BASE = 'api/' + API_VERSION + '/'
API_ROOT = Path(BASE_DIR) / API_NAME
CONTACT_EMAIL = "andreas.garcia@bodzify.com"
UUID_LEN = 22
USER_LIB_DIR_NAME_PREFIXE = "user_"
USER_MAX_NUMBER = "10000000"  # hehe
LIB_TRACK_FILE_SIZE_MIN_IN_MO = 0
LIB_TRACK_FILE_SIZE_MAX_IN_MO = 300
LIB_TRACK_FILE_EXTENSIONS = ['mp3', 'flac', 'wav']
LIB_TRACK_FILE_CONTENT_TYPES = ['audio/mpeg', 'audio/flac', 'audio/wav']
LIB_TRACK_FILENAME_LEN_MAX = 150
LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH = 20
LIB_TRACK_TITLE_LEN_MAX = 200
LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE = ['myfreemp3.vip', 'myfreemp3']  # The order matters
LIB_TRACK_GENERATED_TITLE_LENGTH = 20
LIB_TRACK_GENERATED_TITLE_PREFIXE = "bodzify_"
LIB_TRACK_RATING_VALUE_MAX = 10
LIB_TRACK_LANGUAGE_LEN_MAX = 200
MINE_TRACK_TITLE_LEN_MAX = 200
MINE_TRACK_RELEASED_ON_LEN_MAX = 20
MINE_TRACK_URL_LEN_MAX = 1000
ALBUM_NAME_LEN_MAX = 200
ALBUM_ARTISTS_FIELD_LEN_MAX = 200
ARTIST_NAME_LEN_MAX = 200
CRITERIA_NAME_LEN_MAX = 200
SIMPLE_PLAYLIST_NAME_LEN_MAX = 200
MUSICBRAINZ_BASE_URL = "https://musicbrainz.org/"
MUSICBRAINZ_RECORDING_URL = MUSICBRAINZ_BASE_URL + "recording/"
MUSICBRAINZ_RECORDING_TITLE_LEN_MAX = 200
MUSICBRAINZ_ARTIST_URL = MUSICBRAINZ_BASE_URL + "artist/"
MUSICBRAINZ_ARTIST_NAME_LEN_MAX = 200

AUDIO_FINGERPRINTER_BASE_URL = "http://127.0.0.1"
AUDIO_FINGERPRINTER_PORT = os.getenv('AUDIO_FINGERPRINTER_PORT')
if AUDIO_FINGERPRINTER_PORT is None and ENV is not ENV_VALUES.BUILD:
    raise Exception("AUDIO_FINGERPRINTER_PORT env variable is not set")
AUDIO_FINGERPRINTER_POST_ENDPOINT = "/fingerprint-audio"
AUDIO_FINGERPRINTER_POST_FULL_URL = AUDIO_FINGERPRINTER_BASE_URL + \
    ":" + AUDIO_FINGERPRINTER_PORT + \
    AUDIO_FINGERPRINTER_POST_ENDPOINT

PAGINATION_LIMIT_OFFSET_DEFAULT = 30

SECURE_SSL_REDIRECT = False

# Before calling a view function, Django starts a transaction.
# If the response is produced without problems, Django commits the transaction.
# If the view produces an exception, Django rolls back the transaction.
ATOMIC_REQUESTS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

ACOUSTID_API_KEY = os.getenv('ACOUSTID_API_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

INSTALLED_APPS = ['django.contrib.admin',
                  'django.contrib.auth',
                  'polymorphic',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django_extensions',
                  'corsheaders',
                  'drf_spectacular',
                  'rest_framework',
                  'rest_framework.authtoken',
                  'rest_framework_simplejwt',
                  'coverage',
                  'drf_multiple_model',
                  'bodzify_api']

MIDDLEWARE = ['bodzify_api.middleware.ExceptionLoggingMiddleware.ExceptionLoggingMiddleware',
              'bodzify_api.middleware.RequestLoggingMiddleware.RequestLoggingMiddleware',
              'django.middleware.security.SecurityMiddleware',
              'corsheaders.middleware.CorsMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware']

ROOT_URLCONF = 'bodzify_api.urls'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_BODZIFY_API_DB_NAME'),
        'USER': os.getenv('DB_BODZIFY_API_USERNAME'),
        'PASSWORD': os.getenv('DB_BODZIFY_API_USER_PASSWORD'),
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
            'context_processors': ['django.template.context_processors.debug',
                                   'django.template.context_processors.request',
                                   'django.contrib.auth.context_processors.auth',
                                   'django.contrib.messages.context_processors.messages'],
        },
    },
]

WSGI_APPLICATION = 'bodzify_api.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
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
    'TITLE': API_NAME,
    'DESCRIPTION': API_DESCRIPTION,
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

STATIC_URL = 'static/'

ALLOWED_HOSTS = []
STATICFILES_DIRS = []
STATIC_ROOT = ''
MEDIA_ROOT = ''
FILE_UPLOAD_TEMP_DIR = ''

if ENV in [ENV_VALUES.DEV, ENV_VALUES.CI_TEST]:
    import bodzify_api.settings.settings_dev_or_github_ci_test as settings_dev_or_github_ci_test
    CORS_ALLOW_ALL_ORIGINS = settings_dev_or_github_ci_test.CORS_ALLOW_ALL_ORIGINS
    ALLOWED_HOSTS = settings_dev_or_github_ci_test.ALLOWED_HOSTS
    MEDIA_ROOT = settings_dev_or_github_ci_test.MEDIA_ROOT
    STATIC_ROOT = settings_dev_or_github_ci_test.STATIC_ROOT
    LOG_PATH = settings_dev_or_github_ci_test.LOG_PATH
    JWT_AUTH = settings_dev_or_github_ci_test.JWT_AUTH
    FILE_UPLOAD_TEMP_DIR = settings_dev_or_github_ci_test.FILE_UPLOAD_TEMP_DIR
elif ENV == ENV_VALUES.TEST:
    import bodzify_api.settings.settings_test as settings_test
    CORS_ALLOWED_ORIGINS = settings_test.CORS_ALLOWED_ORIGINS
    SESSION_COOKIE_SECURE = settings_test.SESSION_COOKIE_SECURE
    CSRF_COOKIE_SECURE = settings_test.CSRF_COOKIE_SECURE
    CSRF_TRUSTED_ORIGINS = settings_test.CSRF_TRUSTED_ORIGINS
    ALLOWED_HOSTS = settings_test.ALLOWED_HOSTS
    MEDIA_ROOT = settings_test.MEDIA_ROOT
    STATIC_ROOT = settings_test.STATIC_ROOT
    LOG_PATH = settings_test.LOG_PATH
    FILE_UPLOAD_TEMP_DIR = settings_test.FILE_UPLOAD_TEMP_DIR
else:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_ROOT = BASE_DIR / 'media'

LIB_DIR_NAME = 'libraries'
LIB_PATH = MEDIA_ROOT / LIB_DIR_NAME

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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'general.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'info': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'info.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'requests_with_trace': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'requests.debug.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'exceptions': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'exceptions.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'requests': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'requests.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'bodzify_api': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'bodzify-api.log',
            'maxBytes': 1024*1024*15,  # 15MB
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
            'handlers': ['general'],
            'level': 'DEBUG',
            'propagate': True
        },
        'info': {
            'handlers': ['info'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['requests_with_trace'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'exceptions': {
            'handlers': ['exceptions', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'request': {
            'handlers': ['requests', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['django'],
            'level': 'INFO',
            'propagate': True
        },
        'bodzify_api': {
            'handlers': ['bodzify_api', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}
