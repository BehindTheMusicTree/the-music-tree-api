#!/usr/bin/env python

import datetime
import json
import os
from pathlib import Path
import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(BASE_DIR / 'env/.env')

CALCULATED_INTERNAL_PATHS_ENV_FILE = BASE_DIR / 'env/.env_calculated_internal_paths'

dotenv.load_dotenv(BASE_DIR / 'env/.env')

IS_APP_EXPOSED = os.getenv('IS_APP_EXPOSED')
if not IS_APP_EXPOSED or IS_APP_EXPOSED not in ['true', 'false']:
    raise EnvironmentError("The IS_APP_EXPOSED variable is not set or is not a boolean")

if IS_APP_EXPOSED == 'true':
    print("The app is exposed.")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    CSRF_TRUSTED_ORIGINS_STR = os.getenv('CSRF_TRUSTED_ORIGINS')
    if not CSRF_TRUSTED_ORIGINS_STR:
        raise EnvironmentError("The CSRF_TRUSTED_ORIGINS variable is not set")

    try:
        loaded_csrf_trusted_origins = json.loads(CSRF_TRUSTED_ORIGINS_STR)
        if not isinstance(loaded_csrf_trusted_origins, list):
            loaded_csrf_trusted_origins = [loaded_csrf_trusted_origins]
        CSRF_TRUSTED_ORIGINS = loaded_csrf_trusted_origins
    except json.JSONDecodeError:
        raise ValueError("CSRF_TRUSTED_ORIGINS_STR must either be a list or an element.")
    except Exception as e:
        raise EnvironmentError("The CSRF_TRUSTED_ORIGINS variable is not a valid element or list.")

    if len(CSRF_TRUSTED_ORIGINS) > 0:
        print("The app is exposed to the following origins:")
        for csrf_trusted_origin in CSRF_TRUSTED_ORIGINS:
            print(str(csrf_trusted_origin))
    else:
        raise EnvironmentError("The app is exposed but no trusted origins are set.")

    ALLOWED_HOSTS_STR = os.getenv('ALLOWED_HOSTS')
    if not ALLOWED_HOSTS_STR:
        raise EnvironmentError("The ALLOWED_HOSTS variable is not set")

    try:
        loaded_allowed_hosts = json.loads(ALLOWED_HOSTS_STR)
        if not isinstance(loaded_allowed_hosts, list):
            loaded_allowed_hosts = [loaded_allowed_hosts]
        ALLOWED_HOSTS = loaded_allowed_hosts
    except json.JSONDecodeError:
        raise ValueError("ALLOWED_HOSTS must either be a list or an element.")
    except Exception as e:
        raise EnvironmentError("The ALLOWED_HOSTS variable is not a valid element or list.")

    if len(ALLOWED_HOSTS) > 0:
        print("The allowed hosts are: ")
        for allowed_host in ALLOWED_HOSTS:
            print(str(allowed_host))
    else:
        raise EnvironmentError("The app is exposed but no allowed host are set.")

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    if not SECRET_KEY:
        raise EnvironmentError("The DJANGO_SECRET_KEY variable is not set")
else:
    ALLOWED_HOSTS = ['127.0.0.1']
    SECRET_KEY = "django-default-secret-when-not-exposed"

CORS_ALLOW_ALL_ORIGINS = True

API_VERSION = 'v1'
APP_NAME = "bodzify_api"
API_DESCRIPTION = "API to handle genre oriented music libraries"
API_ROOT_BASE = 'api/' + API_VERSION + '/'
API_ROOT = Path(BASE_DIR) / APP_NAME
CONTACT_EMAIL = "andreas.garcia@bodzify.com"
UUID_LEN = 22
USER_LIBRARIES_DIR_NAME_PREFIXE = "user_"
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

PAGINATION_LIMIT_OFFSET_DEFAULT = 30

SECURE_SSL_REDIRECT = False

# Before calling a view function, Django starts a transaction.
# If the response is produced without problems, Django commits the transaction.
# If the view produces an exception, Django rolls back the transaction.
ATOMIC_REQUESTS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')
if not DEBUG or DEBUG not in ['true', 'false']:
    raise EnvironmentError("The DEBUG variable is not set or is not a boolean")

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
                  APP_NAME]

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

DB_BODZIFY_API_DB_NAME = os.getenv('DB_BODZIFY_API_DB_NAME')
if DB_BODZIFY_API_DB_NAME is None:
    raise EnvironmentError("The DB_BODZIFY_API_DB_NAME variable is not set")

DB_BODZIFY_API_USERNAME = os.getenv('DB_BODZIFY_API_USERNAME')
if DB_BODZIFY_API_USERNAME is None:
    raise EnvironmentError("The DB_BODZIFY_API_USERNAME variable is not set")

DB_BODZIFY_API_USER_PASSWORD = os.getenv('DB_BODZIFY_API_USER_PASSWORD')
if DB_BODZIFY_API_USER_PASSWORD is None:
    raise EnvironmentError("The DB_BODZIFY_API_USER_PASSWORD variable is not set")

DB_HOST = os.getenv('DB_HOST')
if DB_HOST is None:
    raise EnvironmentError("The DB_HOST variable is not set")

DB_PORT = os.getenv('DB_PORT')
if DB_PORT is None:
    raise EnvironmentError("The DB_PORT variable is not set")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_BODZIFY_API_DB_NAME,
        'USER': DB_BODZIFY_API_USERNAME,
        'PASSWORD': DB_BODZIFY_API_USER_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
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
    'TITLE': APP_NAME,
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

AUDIO_META_ANALYSE_NEEDED_STR = os.getenv('AUDIO_META_ANALYSE_NEEDED')
if not AUDIO_META_ANALYSE_NEEDED_STR or AUDIO_META_ANALYSE_NEEDED_STR not in ['true', 'false']:
    raise EnvironmentError("The AUDIO_META_ANALYSE_NEEDED variable is not set or is not a boolean")
AUDIO_META_ANALYSE_NEEDED = True if AUDIO_META_ANALYSE_NEEDED_STR == 'true' else False
print("AUDIO_META_ANALYSE_NEEDED: " + str(AUDIO_META_ANALYSE_NEEDED))

EXTERNAL_DIRS_NEEDED_STR = os.getenv('EXTERNAL_DIRS_NEEDED')
if not EXTERNAL_DIRS_NEEDED_STR or EXTERNAL_DIRS_NEEDED_STR not in ['true', 'false']:
    raise EnvironmentError("The AUDIO_META_ANALYSE_NEEDED variable is not set or is not a boolean")
EXTERNAL_DIRS_NEEDED = True if EXTERNAL_DIRS_NEEDED_STR == 'true' else False
print("EXTERNAL_DIRS_NEEDED: " + str(EXTERNAL_DIRS_NEEDED))

if AUDIO_META_ANALYSE_NEEDED:
    TMP_UPLOADED_FILES_DIR_ENV = os.getenv('TMP_UPLOADED_FILES_DIR')
    if TMP_UPLOADED_FILES_DIR_ENV is None:
        if EXTERNAL_DIRS_NEEDED:
            raise EnvironmentError("The TMP_UPLOADED_FILES_DIR variable is not set while external dirs are needed.")
        else:
            TMP_UPLOADED_FILES_DIR = BASE_DIR / DEFAULT_INTERNAL_PATHS[DEFAULT_INTERNAL_PATHS_KEYS.TMP_UPLOADED_FILES]
    else:
        TMP_UPLOADED_FILES_DIR = Path(TMP_UPLOADED_FILES_DIR_ENV)

    AUDIO_FINGERPRINTER_PORT = os.getenv('AUDIO_FINGERPRINTER_PORT')
    if AUDIO_FINGERPRINTER_PORT is None:
        raise Exception("AUDIO_FINGERPRINTER_PORT env variable is not set")

    AUDIO_FINGERPRINTER_POST_ENDPOINT = os.getenv('AUDIO_FINGERPRINTER_POST_ENDPOINT')
    if AUDIO_FINGERPRINTER_POST_ENDPOINT is None:
        raise Exception("AUDIO_FINGERPRINTER_POST_ENDPOINT env variable is not set")

    AUDIO_FINGERPRINTER_POST_FULL_URL = AUDIO_FINGERPRINTER_BASE_URL + \
        ":" + AUDIO_FINGERPRINTER_PORT + '/' + AUDIO_FINGERPRINTER_POST_ENDPOINT

    ACOUSTID_API_KEY = os.getenv('ACOUSTID_API_KEY')
    if not ACOUSTID_API_KEY and AUDIO_META_ANALYSE_NEEDED:
        raise EnvironmentError("The ACOUSTID_API_KEY variable is not set")

if EXTERNAL_DIRS_NEEDED:
    MEDIA_DIR_ENV = os.getenv('MEDIA_DIR')
    if MEDIA_DIR_ENV is None:
        raise EnvironmentError("The MEDIA_DIR variable is not set")
    else:
        MEDIA_ROOT = Path(MEDIA_DIR_ENV)
        print("Setting media root to: " + str(MEDIA_ROOT))

    LOG_DIR_ENV = os.getenv('DJANGO_LOG_DIR')
    if LOG_DIR_ENV is None:
        raise EnvironmentError("The DJANGO_LOG_DIR variable is not set")
    else:
        LOG_DIR = Path(LOG_DIR_ENV)
        print("Setting log dir to: " + str(LOG_DIR))

    STATIC_FILES_DIR_ENV = os.getenv('STATIC_FILES_DIR')
    if STATIC_FILES_DIR_ENV is None:
        raise EnvironmentError("The STATIC_FILES_DIR variable is not set")
    else:
        STATIC_ROOT = Path(STATIC_FILES_DIR_ENV)
        print("Setting static files dir to: " + str(STATIC_ROOT))
else:
    MEDIA_ROOT = BASE_DIR / DEFAULT_INTERNAL_PATHS[DEFAULT_INTERNAL_PATHS_KEYS.MEDIA]
    print("Setting media dir to default: " + str(MEDIA_ROOT))

    LOG_DIR = BASE_DIR / DEFAULT_INTERNAL_PATHS[DEFAULT_INTERNAL_PATHS_KEYS.LOG]
    print("Setting log dir to default: " + str(LOG_DIR))

    STATIC_ROOT = BASE_DIR / DEFAULT_INTERNAL_PATHS[DEFAULT_INTERNAL_PATHS_KEYS.STATIC_FILES]
    print("Setting static files dir to default: " + str(STATIC_ROOT))

LIBRARIES_DIR_NAME_ENV = os.getenv('LIBRARIES_DIR_NAME')
if LIBRARIES_DIR_NAME_ENV is None:
    if EXTERNAL_DIRS_NEEDED:
        raise EnvironmentError("The LIBRARIES_DIR_NAME variable is not set while external dirs are needed.")
    else:
        LIBRARIES_DIR_NAME = DEFAULT_INTERNAL_PATHS[DEFAULT_INTERNAL_PATHS_KEYS.LIBRARIES_DIR_NAME]
else:
    LIBRARIES_DIR_NAME = LIBRARIES_DIR_NAME_ENV

LIBRARIES_DIR = MEDIA_ROOT / LIBRARIES_DIR_NAME

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
            'filename': LOG_DIR / 'general.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'info': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'info.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'requests_with_trace': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'requests.debug.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'exceptions': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'exceptions.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'requests': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'requests.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        APP_NAME: {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'bodzify-api.log',
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
        APP_NAME: {
            'handlers': [APP_NAME, 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}
