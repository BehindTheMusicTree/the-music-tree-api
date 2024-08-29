#!/usr/bin/env python

import datetime
import json
import os
from pathlib import Path
import subprocess
import dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

APP_ENV_FILE_RELATIVE_PATH = os.getenv('ENV_FILE', 'env/.env')
APP_ENV_FILE = BASE_DIR / APP_ENV_FILE_RELATIVE_PATH
if not APP_ENV_FILE.exists():
    print("No env file at {APP_ENV_FILE}")
    APP_ENV_FILE = None
else:
    print("Env file provided. Loading.")
    dotenv.load_dotenv(APP_ENV_FILE)

CALCULATED_PATHS_ENV_FILE = BASE_DIR / 'env/calculated_paths/.env'
generate_calculated_paths_env_file_script_path = BASE_DIR / 'scripts/generate_calculated_paths_env_file.sh'
try:
    result = subprocess.run(['bash', str(generate_calculated_paths_env_file_script_path),
                             str(BASE_DIR) + '/',
                             CALCULATED_PATHS_ENV_FILE,
                             APP_ENV_FILE or ""],
                            check=True,
                            stderr=subprocess.PIPE,
                            text=True,
                            env=os.environ.copy())
    print("Paths env file generated.")
except subprocess.CalledProcessError as e:
    print("Error while generating the paths env file:", e.stderr)
    raise EnvironmentError("Error while generating the paths env file: " + str(e)) from e

dotenv.load_dotenv(CALCULATED_PATHS_ENV_FILE)

API_VERSION = os.getenv('API_VERSION')
if not API_VERSION:
    raise EnvironmentError("The API_VERSION variable must be set")

APP_IS_EXPOSED_STR = os.getenv('APP_IS_EXPOSED')
if not APP_IS_EXPOSED_STR:
    raise EnvironmentError("The APP_IS_EXPOSED variable must be set")
APP_IS_EXPOSED_STR = APP_IS_EXPOSED_STR.lower()
if APP_IS_EXPOSED_STR not in ['true', 'false']:
    raise EnvironmentError("The APP_IS_EXPOSED variable is not a boolean")
APP_IS_EXPOSED = (APP_IS_EXPOSED_STR == 'true')
if APP_IS_EXPOSED:
    print("APP_IS_EXPOSED is true. Setting up security.")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    CSRF_TRUSTED_ORIGINS_STR = os.getenv('CSRF_TRUSTED_ORIGINS')
    if not CSRF_TRUSTED_ORIGINS_STR:
        raise EnvironmentError("The CSRF_TRUSTED_ORIGINS variable must be set")

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
        raise EnvironmentError("The ALLOWED_HOSTS variable must be set")

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
        raise EnvironmentError("The DJANGO_SECRET_KEY variable must be set")
else:
    ALLOWED_HOSTS = ['127.0.0.1']
    SECRET_KEY = "django-default-secret-when-not-exposed"

CORS_ALLOW_ALL_ORIGINS = True

APP_NAME = os.getenv('APP_NAME')
if not APP_NAME:
    raise EnvironmentError("The APP_NAME variable must be set")

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
MUSICBRAINZ_LOOKUP_ERROR_STR_LEN_MAX = 255
MUSICBRAINZ_ARTIST_URL = MUSICBRAINZ_BASE_URL + "artist/"
MUSICBRAINZ_ARTIST_NAME_LEN_MAX = 200

AUDIO_FINGERPRINTER_BASE_URL = "http://127.0.0.1"

PAGINATION_LIMIT_OFFSET_DEFAULT = 30

SECURE_SSL_REDIRECT = False

# Before calling a view function, Django starts a transaction.
# If the response is produced without problems, Django commits the transaction.
# If the view produces an exception, Django rolls back the transaction.
ATOMIC_REQUESTS = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')
if not DEBUG or DEBUG not in ['true', 'false']:
    raise EnvironmentError("The DEBUG variable is not set or is not a boolean")

INSTALLED_APPS = ['django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django_extensions',
                  'polymorphic',
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

# DB may not be necessary (running collectstati for instance)
DB_IS_NEEDED_STR = os.getenv('DB_IS_NEEDED')
if not DB_IS_NEEDED_STR:
    raise EnvironmentError("The DB_IS_NEEDED variable must be set")
DB_IS_NEEDED_STR = DB_IS_NEEDED_STR.lower()
if DB_IS_NEEDED_STR not in ['true', 'false']:
    raise EnvironmentError("The DB_IS_NEEDED is not a boolean")
DB_IS_NEEDED = True if DB_IS_NEEDED_STR == 'true' else False

if DB_IS_NEEDED:
    DB_BODZIFY_API_DB_NAME = os.getenv('DB_BODZIFY_API_DB_NAME')
    if DB_BODZIFY_API_DB_NAME is None:
        raise EnvironmentError("The DB_BODZIFY_API_DB_NAME variable must be set")

    DB_BODZIFY_API_USERNAME = os.getenv('DB_BODZIFY_API_USERNAME')
    if DB_BODZIFY_API_USERNAME is None:
        raise EnvironmentError("The DB_BODZIFY_API_USERNAME variable must be set")

    DB_BODZIFY_API_USER_PASSWORD = os.getenv('DB_BODZIFY_API_USER_PASSWORD')
    if DB_BODZIFY_API_USER_PASSWORD is None:
        raise EnvironmentError("The DB_BODZIFY_API_USER_PASSWORD variable must be set")

    DB_HOST = os.getenv('DB_HOST')
    if DB_HOST is None:
        raise EnvironmentError("The DB_HOST variable must be set")

    DB_PORT = os.getenv('DB_PORT')
    if DB_PORT is None:
        raise EnvironmentError("The DB_PORT variable must be set")

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

ALLOWED_HOSTS = []
STATICFILES_DIRS = []
STATIC_ROOT = ''
MEDIA_ROOT = ''

AUDIO_META_ANALYSE_IS_NEEDED_STR = os.getenv('AUDIO_META_ANALYSE_IS_NEEDED')
if not AUDIO_META_ANALYSE_IS_NEEDED_STR or AUDIO_META_ANALYSE_IS_NEEDED_STR not in ['true', 'false']:
    raise EnvironmentError("The AUDIO_META_ANALYSE_IS_NEEDED variable is not set or is not a boolean")
AUDIO_META_ANALYSE_IS_NEEDED = True if AUDIO_META_ANALYSE_IS_NEEDED_STR == 'true' else False
print("AUDIO_META_ANALYSE_IS_NEEDED: " + str(AUDIO_META_ANALYSE_IS_NEEDED))

if AUDIO_META_ANALYSE_IS_NEEDED:
    AUDIO_FINGERPRINTER_CONTAINER_NAME = os.getenv('AUDIO_FINGERPRINTER_CONTAINER_NAME')
    if not AUDIO_FINGERPRINTER_CONTAINER_NAME:
        raise EnvironmentError("The AUDIO_FINGERPRINTER_CONTAINER_NAME variable must be set")

    TMP_UPLOADED_FILES_DIR_ENV = os.getenv('TMP_UPLOADED_FILES_DIR')
    if not TMP_UPLOADED_FILES_DIR_ENV:
        raise EnvironmentError("The TMP_UPLOADED_FILES_DIR variable must be set")
    FILE_UPLOAD_TEMP_DIR = Path(TMP_UPLOADED_FILES_DIR_ENV)  # Django constant, do not rename.
    print("FILE_UPLOAD_TEMP_DIR: " + str(FILE_UPLOAD_TEMP_DIR))

    AUDIO_FINGERPRINTER_PORT = os.getenv('AUDIO_FINGERPRINTER_PORT')
    if AUDIO_FINGERPRINTER_PORT is None:
        raise Exception("AUDIO_FINGERPRINTER_PORT env variable must be set")

    AUDIO_FINGERPRINTER_POST_ENDPOINT = os.getenv('AUDIO_FINGERPRINTER_POST_ENDPOINT')
    if AUDIO_FINGERPRINTER_POST_ENDPOINT is None:
        raise Exception("AUDIO_FINGERPRINTER_POST_ENDPOINT env variable must be set")

    AUDIO_FINGERPRINTER_POST_FULL_URL = AUDIO_FINGERPRINTER_BASE_URL + \
        ":" + AUDIO_FINGERPRINTER_PORT + '/' + AUDIO_FINGERPRINTER_POST_ENDPOINT

    ACOUSTID_API_KEY = os.getenv('ACOUSTID_API_KEY')
    if not ACOUSTID_API_KEY and AUDIO_META_ANALYSE_IS_NEEDED:
        raise EnvironmentError("The ACOUSTID_API_KEY variable must be set")

STATIC_FILES_ARE_NEEDED_STR = os.getenv('STATIC_FILES_ARE_NEEDED')
if not STATIC_FILES_ARE_NEEDED_STR or STATIC_FILES_ARE_NEEDED_STR not in ['true', 'false']:
    raise EnvironmentError("The STATIC_FILES_ARE_NEEDED variable is not set or is not a boolean")
STATIC_FILES_ARE_NEEDED = True if STATIC_FILES_ARE_NEEDED_STR == 'true' else False

if STATIC_FILES_ARE_NEEDED:
    print("STATIC_FILES_ARE_NEEDED is true. Setting up static files.")
    STATIC_URL = 'static/'
    STATIC_FILES_DIR_ENV = os.getenv('STATIC_FILES_DIR')
    if not STATIC_FILES_DIR_ENV:
        raise EnvironmentError("The STATIC_FILES_DIR variable must be set")
    STATIC_ROOT = Path(STATIC_FILES_DIR_ENV)
else:
    print("Static files are not needed.")

MEDIA_DIR_ENV = os.getenv('MEDIA_DIR')
if not MEDIA_DIR_ENV:
    raise EnvironmentError("The MEDIA_DIR variable must be set")
MEDIA_ROOT = Path(MEDIA_DIR_ENV)  # Django constant, do not rename.
print("MEDIA_ROOT: " + str(MEDIA_ROOT))

LIBRARIES_DIR_NAME = os.getenv('LIBRARIES_DIR_NAME')
if not LIBRARIES_DIR_NAME:
    raise EnvironmentError("The LIBRARIES_DIR_NAME variable must be set")
LIBRARIES_DIR = MEDIA_ROOT / LIBRARIES_DIR_NAME
print("LIBRARIES_DIR: " + str(LIBRARIES_DIR))

LOGS_ARE_NEEDED_STR = os.getenv('DJANGO_LOGS_ARE_NEEDED')
if not LOGS_ARE_NEEDED_STR:
    raise EnvironmentError("The LOGS_ARE_NEEDED variable must be set")
LOGS_ARE_NEEDED_STR = LOGS_ARE_NEEDED_STR.lower()
if LOGS_ARE_NEEDED_STR not in ['true', 'false']:
    raise EnvironmentError("The LOGS_ARE_NEEDED variable is not set or is not a boolean")
LOGS_ARE_NEEDED = (LOGS_ARE_NEEDED_STR == 'true')

if LOGS_ARE_NEEDED:
    print("DJANGO_LOGS_ARE_NEEDED is true. Setting up logs.")
    LOG_DIR_ENV = os.getenv('DJANGO_LOG_DIR')
    if not LOG_DIR_ENV:
        raise EnvironmentError("The DJANGO_LOG_DIR variable must be set")
    LOG_DIR = Path(LOG_DIR_ENV)

    LOG_GENERAL_FILENAME = os.getenv('DJANGO_LOG_GENERAL_FILENAME')
    if not LOG_GENERAL_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_GENERAL_FILENAME variable must be set")

    LOG_INFO_FILENAME = os.getenv('DJANGO_LOG_INFO_FILENAME')
    if not LOG_INFO_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_INFO_FILENAME variable must be set")

    LOG_REQUESTS_FILENAME = os.getenv('DJANGO_LOG_REQUESTS_FILENAME')
    if not LOG_REQUESTS_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_REQUESTS_FILENAME variable must be set")

    LOG_REQUESTS_DEBUG_FILENAME = os.getenv('DJANGO_LOG_REQUESTS_DEBUG_FILENAME')
    if not LOG_REQUESTS_DEBUG_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_REQUESTS_DEBUG_FILENAME variable must be set")

    LOG_EXCEPTIONS_FILENAME = os.getenv('DJANGO_LOG_EXCEPTIONS_FILENAME')
    if not LOG_EXCEPTIONS_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_EXCEPTIONS_FILENAME variable must be set")

    LOG_DJANGO_FILENAME = os.getenv('DJANGO_LOG_DJANGO_FILENAME')
    if not LOG_DJANGO_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_DJANGO_FILENAME variable must be set")

    LOG_APP_FILENAME = os.getenv('DJANGO_LOG_APP_FILENAME')
    if not LOG_APP_FILENAME:
        raise EnvironmentError("The DJANGO_LOG_APP_FILENAME variable must be set")

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
                'filename': LOG_DIR / LOG_GENERAL_FILENAME,
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
                'formatter': 'standard'
            },
            'info': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / LOG_INFO_FILENAME,
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
                'formatter': 'standard'
            },
            'requests': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / LOG_REQUESTS_FILENAME,
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
                'formatter': 'standard'
            },
            'requests_with_trace': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / LOG_REQUESTS_DEBUG_FILENAME,
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
                'formatter': 'standard'
            },
            'exceptions': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / LOG_EXCEPTIONS_FILENAME,
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
                'formatter': 'standard'
            },
            'django': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / LOG_DJANGO_FILENAME,
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
                'formatter': 'standard'
            },
            APP_NAME: {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / LOG_APP_FILENAME,
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
else:
    print("Logs are not needed.")
