
import datetime
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from bodzify_api.utils.AppStaticFileStates import StaticFileStates
from bodzify_api.utils.env_var_loader import (
    load_calculated_env_paths, load_env_vars_from_file_if_exists,
    load_required_bool_env_var, load_required_path_env_var,
    load_required_secret_env_var, load_required_str_env_var)
from bodzify_api.utils.utils import print_django

TEST_USER_LIBRARIES_DIR_NAME_PREFIXE: str
USER_MAX_NUMBER: str
UUID_LEN: int
FILE_PATH_MAX_LENGTH: int
LIB_TRACK_FILE_SIZE_MIN_IN_MO: int
LIB_TRACK_FILE_SIZE_MAX_IN_MO: int
LIB_TRACK_FILE_EXTENSIONS: List[str] = []
LIB_TRACK_FILE_CONTENT_TYPES: List[str] = []
LIB_TRACK_FILENAME_LEN_MAX: int
LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH: int
LIB_TRACK_TITLE_LEN_MAX: int
LIB_TRACK_TRACK_NUMBER_MAX: int
LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE: List[str] = []
LIB_TRACK_GENERATED_TITLE_LENGTH: int
LIB_TRACK_GENERATED_TITLE_PREFIXE: str
LIB_TRACK_RATING_VALUE_MAX: int
LIB_TRACK_LANGUAGE_LEN_MAX: int
MINE_TRACK_TITLE_LEN_MAX: int
MINE_TRACK_RELEASED_ON_LEN_MAX: int
MINE_TRACK_URL_LEN_MAX: int
ALBUM_NAME_LEN_MAX: int
ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX: int
ARTIST_NAME_LEN_MAX: int
ARTISTS_NAMES_LEN_MAX: int
CRITERIA_TYPE_LABEL_LEN_MAX: int
CRITERIA_NAME_LEN_MAX: int
MANUAL_PLAYLIST_NAME_LEN_MAX: int
FINGERPRINTING_ERROR_MESSAGE_LEN_MAX: int
FINGERPRINTING_ERROR_CODE_LABEL_LEN_MAX: int
MUSICBRAINZ_BASE_URL: str
MUSICBRAINZ_ID_LEN_MAX: int
MUSICBRAINZ_RECORDING_URL: str
MUSICBRAINZ_RECORDING_TITLE_LEN_MAX: int
MUSICBRAINZ_RECORDING_MISSING_CAUSE_CODE_LABEL_LEN_MAX: int
MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX: int
MUSICBRAINZ_ARTIST_URL: str
MUSICBRAINZ_ARTIST_NAME_LEN_MAX: int
PAGINATION_LIMIT_OFFSET_DEFAULT: int

# AFP Connection
AFP_POST_FULL_URL: str

# Static Files
STATIC_ROOT: Path
STATIC_URL: str

# Installed Apps and Caches
INSTALLED_APPS: List[str] = []
CACHES: Dict[str, Any] = {}

# Middleware
MIDDLEWARE: List[str] = []

# Templates
TEMPLATES: List[Dict[str, Any]] = []

# Django Constants
WSGI_APPLICATION: str
AUTH_USER_MODEL: str
AUTH_PASSWORD_VALIDATORS: List[Dict[str, Any]] = []
LANGUAGE_CODE: str
TIME_ZONE: str
USE_I18N: bool
USE_TZ: bool
DEFAULT_AUTO_FIELD: str
REST_FRAMEWORK: Dict[str, Any] = {}
SPECTACULAR_SETTINGS: Dict[str, Any] = {}
SIMPLE_JWT: Dict[str, Any] = {}

# Media
ACOUSTID_API_KEY: str
MEDIA_ROOT: Path
MEDIA_URL: str
LIBRARIES_DIR_NAME: str
LIBRARIES_DIR: Path

# Secret Key
SECRET_KEY: str

# File Upload
FILE_UPLOAD_TEMP_DIR: str | None
FILE_UPLOAD_ENABLED: bool


def init_logs_if_needed():
    from bodzify_api.logging.LoggersName import LoggersName

    LOG_DIR_STR = os.getenv('DJANGO_LOG_DIR')
    if not LOG_DIR_STR:
        print_django("The DJANGO_LOG_DIR variable is not set. Logs will not be set up.")
    else:
        print_django("LOG_DIR is set. Setting up logs...")

        LOG_DIR = Path(LOG_DIR_STR)
        if not LOG_DIR.exists():
            raise EnvironmentError(f"The log directory {LOG_DIR} does not exist.")
        print_django(f"The log dir {LOG_DIR} exists.")

        LOG_GENERAL_FILENAME = load_required_str_env_var('DJANGO_LOG_GENERAL_FILENAME')
        LOG_GENERAL_FILE = LOG_DIR / LOG_GENERAL_FILENAME
        if not LOG_GENERAL_FILE.exists():
            raise EnvironmentError(f"The log general file {LOG_GENERAL_FILE} does not exist.")
        print_django("The log general file {LOG_GENERAL_FILE} exists.")

        LOG_INFO_FILENAME = load_required_str_env_var('DJANGO_LOG_INFO_FILENAME')
        LOG_INFO_FILE = LOG_DIR / LOG_INFO_FILENAME
        if not LOG_INFO_FILE.exists():
            raise EnvironmentError(f"The log info file {LOG_INFO_FILE} does not exist.")
        print_django(f"The log info file {LOG_INFO_FILE} exists.")

        LOG_REQUESTS_FILENAME = load_required_str_env_var('DJANGO_LOG_REQUESTS_FILENAME')
        LOG_REQUESTS_FILE = LOG_DIR / LOG_REQUESTS_FILENAME
        if not LOG_REQUESTS_FILE.exists():
            raise EnvironmentError(f"The log requests file {LOG_REQUESTS_FILE} does not exist.")
        print_django(f"The log info file {LOG_REQUESTS_FILE} exists.")

        LOG_REQUESTS_DEBUG_FILENAME = load_required_str_env_var('DJANGO_LOG_REQUESTS_DEBUG_FILENAME')
        LOG_REQUESTS_DEBUG_FILE = LOG_DIR / LOG_REQUESTS_DEBUG_FILENAME
        if not LOG_REQUESTS_DEBUG_FILE.exists():
            raise EnvironmentError(f"The log requests debug file {LOG_REQUESTS_DEBUG_FILE} does not exist.")
        print_django(f"The log info file {LOG_REQUESTS_DEBUG_FILE} exists.")

        LOG_EXCEPTIONS_FILENAME = load_required_str_env_var('DJANGO_LOG_EXCEPTIONS_FILENAME')
        LOG_EXCEPTIONS_FILE = LOG_DIR / LOG_EXCEPTIONS_FILENAME
        if not LOG_EXCEPTIONS_FILE.exists():
            raise EnvironmentError(f"The log exceptions file {LOG_EXCEPTIONS_FILE} does not exist.")
        print_django(f"The log info file {LOG_EXCEPTIONS_FILE} exists.")

        LOG_DJANGO_FILENAME = load_required_str_env_var('DJANGO_LOG_DJANGO_FILENAME')
        LOG_DJANGO_FILE = LOG_DIR / LOG_DJANGO_FILENAME
        if not LOG_DJANGO_FILE.exists():
            raise EnvironmentError(f"The log django file {LOG_DJANGO_FILE} does not exist.")
        print_django(f"The log info file {LOG_DJANGO_FILE} exists.")

        LOG_APP_FILENAME = load_required_str_env_var('DJANGO_LOG_APP_FILENAME')
        LOG_APP_FILE = LOG_DIR / LOG_APP_FILENAME
        if not LOG_APP_FILE.exists():
            raise EnvironmentError(f"The log app file {LOG_APP_FILE} does not exist.")
        print_django(f"The log info file {LOG_APP_FILE} exists.")

        class LOGGERS_NAME:
            INFO = 'info'
            REQUEST = 'request'
            REQUEST_DJANGO = 'django.request'
            EXCEPTIONS = 'exceptions'
            DJANGO = 'django'
            APP = APP_NAME

        global LOGGING
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s]- %(message)s'
                }
            },
            'handlers': {
                'general': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_GENERAL_FILE,
                    'maxBytes': 1024*1024*15,  # 15MB
                    'backupCount': 10,
                    'formatter': 'standard'
                },
                'info': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_INFO_FILE,
                    'maxBytes': 1024*1024*15,  # 15MB
                    'backupCount': 10,
                    'formatter': 'standard'
                },
                'requests': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_REQUESTS_FILE,
                    'maxBytes': 1024*1024*15,  # 15MB
                    'backupCount': 10,
                    'formatter': 'standard'
                },
                'requests_with_trace': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_REQUESTS_DEBUG_FILE,
                    'maxBytes': 1024*1024*15,  # 15MB
                    'backupCount': 10,
                    'formatter': 'standard'
                },
                'exceptions': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_EXCEPTIONS_FILE,
                    'maxBytes': 1024*1024*15,  # 15MB
                    'backupCount': 10,
                    'formatter': 'standard'
                },
                'django': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_DJANGO_FILE,
                    'maxBytes': 1024*1024*15,  # 15MB
                    'backupCount': 10,
                    'formatter': 'standard'
                },
                APP_NAME: {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': LOG_APP_FILE,
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
                LoggersName.INFO: {
                    'handlers': ['info'],
                    'level': 'DEBUG',
                    'propagate': True
                },
                LoggersName.REQUEST: {
                    'handlers': ['requests', 'console'],
                    'level': 'INFO',
                    'propagate': True,
                },
                LoggersName.REQUEST_DJANGO: {
                    'handlers': ['requests_with_trace'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
                LoggersName.EXCEPTIONS: {
                    'handlers': ['exceptions', 'console'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
                LoggersName.DJANGO: {
                    'handlers': ['django'],
                    'level': 'INFO',
                    'propagate': True
                },
                LoggersName.APP: {
                    'handlers': [APP_NAME, 'console'],
                    'level': 'DEBUG',
                    'propagate': True
                },
            },
        }
        print_django("Logs are set up.")


def setup_app_exposure_if_needed():
    global ALLOWED_HOSTS

    APP_VERSION = load_required_str_env_var('APP_VERSION')
    global API_ROOT_BASE
    API_ROOT_BASE = 'api/' + APP_VERSION + '/'
    print_django("API_ROOT_BASE: " + API_ROOT_BASE)

    global ROOT_URLCONF
    ROOT_URLCONF = f'{APP_NAME}.urls'

    if APP_IS_EXPOSED:
        print_django("APP_IS_EXPOSED is true. Setting up security.")
        global SECURE_SSL_REDIRECT
        SECURE_SSL_REDIRECT = False
        print_django(f"SECURE_SSL_REDIRECT: {SECURE_SSL_REDIRECT}")
        global SESSION_COOKIE_SECURE
        SESSION_COOKIE_SECURE = True
        print_django(f"SESSION_COOKIE_SECURE: {SESSION_COOKIE_SECURE}")
        global CSRF_COOKIE_SECURE
        CSRF_COOKIE_SECURE = True
        print_django(f"CSRF_COOKIE_SECURE: {CSRF_COOKIE_SECURE}")

        CSRF_TRUSTED_ORIGINS_STR = load_required_str_env_var('CSRF_TRUSTED_ORIGINS')
        print_django(f"CSRF_TRUSTED_ORIGINS env variable: {CSRF_TRUSTED_ORIGINS_STR}")
        global CSRF_TRUSTED_ORIGINS
        CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS_STR.split(',')
        for csrf_trusted_origin in CSRF_TRUSTED_ORIGINS:
            csrf_trusted_origin = csrf_trusted_origin.strip()
            if csrf_trusted_origin == '':
                raise ValueError("An CSRF trusted origin is empty.")
        if len(CSRF_TRUSTED_ORIGINS) > 0:
            print_django("The app is exposed to the following origin(s):")
            for csrf_trusted_origin in CSRF_TRUSTED_ORIGINS:
                print_django(str(csrf_trusted_origin))
        else:
            raise EnvironmentError("The app is exposed but no trusted origins are set.")

        ALLOWED_HOSTS_STR = load_required_str_env_var('ALLOWED_HOSTS')
        ALLOWED_HOSTS = ALLOWED_HOSTS_STR.split(',')
        for csrf_trusted_origin in ALLOWED_HOSTS:
            csrf_trusted_origin = csrf_trusted_origin.strip()
            if csrf_trusted_origin == '':
                raise ValueError("An allowed host is empty.")
        if len(ALLOWED_HOSTS) > 0:
            print_django("Allowed host(s): ")
            for csrf_trusted_origin in ALLOWED_HOSTS:
                print_django(str(csrf_trusted_origin))
        else:
            raise EnvironmentError("The app is exposed but no allowed hosts are set.")

        print_django(f"CORS_ALLOW_ALL_ORIGINS is not set as a web server is used to handle CORS.")
    else:
        ALLOWED_HOSTS = ['127.0.0.1']
        global CORS_ALLOW_ALL_ORIGINS
        CORS_ALLOW_ALL_ORIGINS = True
        print_django(f"CORS_ALLOW_ALL_ORIGINS is set to: {CORS_ALLOW_ALL_ORIGINS}")

    print_django(f"ALLOWED_HOSTS is set to {ALLOWED_HOSTS}")


def setup_app_constants():
    # Before calling a view function, Django starts a transaction.
    # If the response is produced without problems, Django commits the transaction.
    # If the view produces an exception, Django rolls back the transaction.
    global ATOMIC_REQUESTS
    ATOMIC_REQUESTS = True

    # SECURITY WARNING: don't run with debug turned on in production!
    global DEBUG
    DEBUG = load_required_bool_env_var('DEBUG')

    global USER_LIBRARIES_DIR_NAME_PREFIXE
    USER_LIBRARIES_DIR_NAME_PREFIXE = "user_"
    global TEST_USER_LIBRARIES_DIR_NAME_PREFIXE
    TEST_USER_LIBRARIES_DIR_NAME_PREFIXE = "test_user_"
    global USER_MAX_NUMBER
    USER_MAX_NUMBER = "10000000"  # hehe

    global UUID_LEN
    UUID_LEN = 36

    global FILE_PATH_MAX_LENGTH
    FILE_PATH_MAX_LENGTH = 255
    global LIB_TRACK_FILE_SIZE_MIN_IN_MO
    LIB_TRACK_FILE_SIZE_MIN_IN_MO = 0
    global LIB_TRACK_FILE_SIZE_MAX_IN_MO
    LIB_TRACK_FILE_SIZE_MAX_IN_MO = 300
    # Set Django's upload size limit to match our max file size
    global DATA_UPLOAD_MAX_MEMORY_SIZE
    DATA_UPLOAD_MAX_MEMORY_SIZE = LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1024 * 1024  # Convert MB to bytes
    global LIB_TRACK_FILE_EXTENSIONS
    LIB_TRACK_FILE_EXTENSIONS = ['mp3', 'flac', 'wav']
    global LIB_TRACK_FILE_CONTENT_TYPES
    LIB_TRACK_FILE_CONTENT_TYPES = ['audio/mpeg', 'audio/flac', 'audio/wav']
    global LIB_TRACK_FILENAME_LEN_MAX
    LIB_TRACK_FILENAME_LEN_MAX = 150
    global LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH
    LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH = 20
    global LIB_TRACK_TITLE_LEN_MAX
    LIB_TRACK_TITLE_LEN_MAX = 200
    global LIB_TRACK_TRACK_NUMBER_MAX
    LIB_TRACK_TRACK_NUMBER_MAX = 1000
    global LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE
    LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE = ['myfreemp3.vip', 'myfreemp3']  # The order matters
    global LIB_TRACK_GENERATED_TITLE_LENGTH
    LIB_TRACK_GENERATED_TITLE_LENGTH = 20
    global LIB_TRACK_GENERATED_TITLE_PREFIXE
    LIB_TRACK_GENERATED_TITLE_PREFIXE = "bodzify_"
    global LIB_TRACK_RATING_VALUE_MAX
    LIB_TRACK_RATING_VALUE_MAX = 10
    global LIB_TRACK_LANGUAGE_LEN_MAX
    LIB_TRACK_LANGUAGE_LEN_MAX = 200

    global MINE_TRACK_TITLE_LEN_MAX
    MINE_TRACK_TITLE_LEN_MAX = 200
    global MINE_TRACK_RELEASED_ON_LEN_MAX
    MINE_TRACK_RELEASED_ON_LEN_MAX = 20
    global MINE_TRACK_URL_LEN_MAX
    MINE_TRACK_URL_LEN_MAX = 1000
    global ALBUM_NAME_LEN_MAX
    ALBUM_NAME_LEN_MAX = 200
    global ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX
    ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX = 200
    global ARTIST_NAME_LEN_MAX
    ARTIST_NAME_LEN_MAX = 200
    global ARTISTS_NAMES_LEN_MAX
    ARTISTS_NAMES_LEN_MAX = 200
    global CRITERIA_TYPE_LABEL_LEN_MAX
    CRITERIA_TYPE_LABEL_LEN_MAX = 200
    global CRITERIA_NAME_LEN_MAX
    CRITERIA_NAME_LEN_MAX = 200
    global MANUAL_PLAYLIST_NAME_LEN_MAX
    MANUAL_PLAYLIST_NAME_LEN_MAX = 200

    global FINGERPRINTING_ERROR_MESSAGE_LEN_MAX
    FINGERPRINTING_ERROR_MESSAGE_LEN_MAX = 200
    global FINGERPRINTING_ERROR_CODE_LABEL_LEN_MAX
    FINGERPRINTING_ERROR_CODE_LABEL_LEN_MAX = 200

    MUSICBRAINZ_BASE_URL = "https://musicbrainz.org/"
    global MUSICBRAINZ_ID_LEN_MAX
    MUSICBRAINZ_ID_LEN_MAX = 36
    global MUSICBRAINZ_RECORDING_URL
    MUSICBRAINZ_RECORDING_URL = MUSICBRAINZ_BASE_URL + "recording/"
    global MUSICBRAINZ_RECORDING_TITLE_LEN_MAX
    MUSICBRAINZ_RECORDING_TITLE_LEN_MAX = 200
    global MUSICBRAINZ_RECORDING_MISSING_CAUSE_CODE_LABEL_LEN_MAX
    MUSICBRAINZ_RECORDING_MISSING_CAUSE_CODE_LABEL_LEN_MAX = 255

    # Needs a large text for messages like:
    # "HTTP request failed: HTTPConnectionPool(host='api.acoustid.org', port=80): Max retries exceeded with url:
    # /v2/lookup (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x10a884170>: Failed to
    # resolve 'api.acoustid.org' ([Errno 8] nodename nor servname provided, or not known)\"))"
    global MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX
    MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX = 400
    global MUSICBRAINZ_ARTIST_URL
    MUSICBRAINZ_ARTIST_URL = MUSICBRAINZ_BASE_URL + "artist/"
    global MUSICBRAINZ_ARTIST_NAME_LEN_MAX
    MUSICBRAINZ_ARTIST_NAME_LEN_MAX = 200
    global PAGINATION_LIMIT_OFFSET_DEFAULT
    PAGINATION_LIMIT_OFFSET_DEFAULT = 30


def setup_afp_connection():
    if APP_IS_EXPOSED:
        print_django("The app is exposed. The AFP host is the AFP container name.")
        AFP_BASE_URL = AFP_CONTAINER_NAME
    else:
        print_django("The app is not exposed. The AFP host is the AFP url.")
        AFP_BASE_URL = load_required_str_env_var('AFP_URL')

    AFP_PORT = load_required_str_env_var('AFP_PORT')
    AFP_POST_ENDPOINT = load_required_str_env_var('AFP_POST_ENDPOINT')

    global AFP_POST_FULL_URL
    AFP_POST_FULL_URL = "http://" + AFP_BASE_URL + ":" + AFP_PORT + '/' + AFP_POST_ENDPOINT
    print_django(f"AFP_POST_FULL_URL: {AFP_POST_FULL_URL}")


def setup_static_files():
    print_django(f"The app is using static files for {STATIC_FILES_STATE}")

    # Django constant, do not rename.
    global STATIC_ROOT
    STATIC_ROOT = Path(STATIC_FILES)  # type: ignore
    print_django("STATIC_ROOT: " + str(STATIC_ROOT))
    if not STATIC_ROOT.exists():
        raise EnvironmentError(f"The static root {STATIC_ROOT} does not exist.")
    print_django(f"The dir {STATIC_ROOT} exists.")

    global STATIC_URL
    STATIC_URL = load_required_str_env_var('STATIC_FILES_URL')
    # STATICFILES_DIRS = [] # No additional static files directories are needed.


def setup_installed_apps_and_caches():
    global INSTALLED_APPS
    INSTALLED_APPS = ['django.contrib.admin',
                      'django.contrib.auth',
                      'django.contrib.contenttypes',
                      'django.contrib.sessions',
                      'django.contrib.messages',
                      'django_extensions',
                      'polymorphic',
                      'corsheaders',
                      'drf_spectacular',
                      'rest_framework',
                      'rest_framework.authtoken',
                      'coverage',
                      'drf_multiple_model',
                      APP_NAME]

    if APP_IS_EXPOSED == True:
        INSTALLED_APPS.append('rest_framework_simplejwt')

    if STATIC_FILES_STATE in [StaticFileStates.COLLECTING, StaticFileStates.SERVING]:
        INSTALLED_APPS.append('django.contrib.staticfiles')

    global CACHES
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }


def setup_middlewares():
    """Setup Django middleware classes."""
    global MIDDLEWARE
    MIDDLEWARE = [
        f'{APP_NAME}.middleware.duplicate_fields.middleware.DuplicateFieldsMiddleware',
        f'{APP_NAME}.middleware.ExceptionLoggingMiddleware.ExceptionLoggingMiddleware',
        f'{APP_NAME}.middleware.RequestLoggingMiddleware.RequestLoggingMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ]


def setup_db_connection():
    DB_BODZIFY_API_DB_NAME = load_required_str_env_var('DB_BODZIFY_API_DB_NAME')
    DB_BODZIFY_API_USERNAME = load_required_str_env_var('DB_BODZIFY_API_USERNAME')
    DB_BODZIFY_API_USER_PASSWORD = load_required_secret_env_var('DB_BODZIFY_API_USER_PASSWORD')

    if APP_IS_EXPOSED:
        print_django("The app is exposed. The db host is the db container name.")
        DB_CONTAINER_NAME = load_required_str_env_var('DB_CONTAINER_NAME')
        DB_HOST = DB_CONTAINER_NAME
    else:
        print_django("The app is not exposed. The db host is the db url.")
        DB_URL = load_required_str_env_var('DB_URL')
        DB_HOST = DB_URL
    print_django(f"DB_HOST: " + DB_HOST)

    DB_PORT = load_required_str_env_var('DB_PORT')

    global DATABASES
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_BODZIFY_API_DB_NAME,
            'USER': DB_BODZIFY_API_USERNAME,
            'PASSWORD': DB_BODZIFY_API_USER_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'DISABLE_SERVER_SIDE_CURSORS': True
        }
    }


def setup_templates():
    global TEMPLATES
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


def setup_django_constants():
    global WSGI_APPLICATION
    WSGI_APPLICATION = f'{APP_NAME}.wsgi.application'

    global AUTH_USER_MODEL
    AUTH_USER_MODEL = f'{APP_NAME}.User'

    global AUTH_PASSWORD_VALIDATORS
    AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                                {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                                {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                                {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }]
    global LANGUAGE_CODE
    LANGUAGE_CODE = 'en-us'
    global TIME_ZONE
    TIME_ZONE = 'UTC'
    global USE_I18N
    USE_I18N = True
    global USE_TZ
    USE_TZ = True
    global DEFAULT_AUTO_FIELD
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    global REST_FRAMEWORK
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

    global SPECTACULAR_SETTINGS
    SPECTACULAR_SETTINGS = {
        'TITLE': APP_NAME,
        'DESCRIPTION': "API to handle genre oriented music libraries",
        'VERSION': '0.1.0',
        'SERVE_INCLUDE_SCHEMA': False,
        'SCHEMA_PATH_PREFIX': '/api/v[0-9]'
    }

    global SIMPLE_JWT
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=100),
        'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
        'AUTH_HEADER_TYPES': ('Bearer',),
    }


def setup_media_dirs():
    print_django("FILE_UPLOAD_TEMP_DIR is set. Setting up the media variables...")

    global ACOUSTID_API_KEY
    ACOUSTID_API_KEY = load_required_secret_env_var('ACOUSTID_API_KEY')

    global MEDIA_ROOT  # Django constant, do not rename.
    MEDIA_ROOT = load_required_path_env_var('MEDIA_DIR')

    if APP_IS_EXPOSED:
        global MEDIA_URL
        MEDIA_URL = load_required_str_env_var('MEDIA_URL')

    global LIBRARIES_DIR_NAME
    LIBRARIES_DIR_NAME = load_required_str_env_var('LIBRARIES_DIR_NAME')

    global LIBRARIES_DIR
    LIBRARIES_DIR = MEDIA_ROOT / LIBRARIES_DIR_NAME
    print_django("LIBRARIES_DIR: " + str(LIBRARIES_DIR))
    if not LIBRARIES_DIR.exists():
        raise EnvironmentError(f"The libraries directory {LIBRARIES_DIR} does not exist.")
    print_django("The LIBRARIES_DIR directory exists.")
    print_django("Media variables are set.")


def set_secret_key():
    global SECRET_KEY
    if APP_IS_EXPOSED:
        # SECURITY WARNING: keep the secret key used in production secret!
        # SECRET_KET is a Django constant, do not rename.
        SECRET_KEY = load_required_secret_env_var('DJANGO_SECRET_KEY')
    else:
        SECRET_KEY = "django_default_secret_when_not_exposed"


BASE_DIR = Path(__file__).resolve().parent.parent

APP_ENV_FILE_RELATIVE_PATH = os.getenv('ENV_FILE', 'env/.env')
APP_ENV_FILE = BASE_DIR / APP_ENV_FILE_RELATIVE_PATH
load_env_vars_from_file_if_exists(APP_ENV_FILE)

ENV = load_required_str_env_var('ENV')
APP_NAME = load_required_str_env_var('APP_NAME')
APP_IS_EXPOSED = load_required_bool_env_var('APP_IS_EXPOSED')

set_secret_key()

if 'pytest' in sys.argv[0]:
    print_django("settings.py is being executed because of a pytest command.")

    if os.environ.get('AUDIO_META_ANALYSIS_ENABLED', 'False').lower() == 'true':
        AUDIO_META_ANALYSIS_ENABLED = True
        print_django("The audio meta analysis is enabled.")
    else:
        AUDIO_META_ANALYSIS_ENABLED = False
        print_django("The audio meta analysis is disabled.")

    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']  # Less secured to speed up tests
else:
    AUDIO_META_ANALYSIS_ENABLED = True
    print_django("settings.py is not being executed because of a pytest command. The audio meta analysis is enabled.")

if 'loaddata' in sys.argv:
    print_django("settings.py is being executed because of a loaddata command.")
    load_calculated_env_paths(BASE_DIR)
    STATIC_FILES_STATE = StaticFileStates.NOT_NEEDED
    setup_app_constants()
    setup_installed_apps_and_caches()
    setup_middlewares()
    setup_django_constants()
    setup_db_connection()
    setup_templates()  # Needed to use the admin application
    setup_media_dirs()  # Needed for the User model library path field
else:
    load_calculated_env_paths(BASE_DIR)
    setup_app_exposure_if_needed()
    setup_app_constants()

    STATIC_FILES = os.getenv('STATIC_FILES')
    if ENV == 'COLLECT_STATIC':
        STATIC_FILES_STATE = StaticFileStates.COLLECTING
        setup_static_files()
    else:
        if not STATIC_FILES:
            print_django("Static files are not needed.")
            STATIC_FILES_STATE = StaticFileStates.NOT_NEEDED
        else:
            print_django("Static files are being served.")
            STATIC_FILES_STATE = StaticFileStates.SERVING
            setup_static_files()

    setup_installed_apps_and_caches()
    setup_middlewares()
    setup_templates()
    setup_django_constants()
    init_logs_if_needed()

    if load_required_bool_env_var('DB_IS_NEEDED'):
        setup_db_connection()

    # FILE_UPLOAD_TEMP_DIR is a Django constant, do not rename.
    FILE_UPLOAD_TEMP_DIR = os.getenv('TMP_UPLOADED_FILES')
    print_django(f"FILE_UPLOAD_TEMP_DIR: {FILE_UPLOAD_TEMP_DIR}")
    if not FILE_UPLOAD_TEMP_DIR:
        print_django("TMP_UPLOADED_FILES/FILE_UPLOAD_TEMP_DIR is not set. The app will not handle media files.")
        FILE_UPLOAD_ENABLED = False
        for var_name in ['AFP_PORT',
                         'AFP_CONTAINER_NAME',
                         'AFP_POST_ENDPOINT',
                         'ACOUSTID_API_KEY',
                         'MEDIA_DIR',
                         'LIBRARIES_DIR_NAME']:
            if os.getenv(var_name):
                raise EnvironmentError(f"The {var_name} env variable cannot be set as \
                    TMP_UPLOADED_FILES/FILE_UPLOAD_TEMP_DIR is not.")
    else:
        FILE_UPLOAD_ENABLED = True
        AFP_CONTAINER_NAME = load_required_str_env_var('AFP_CONTAINER_NAME')
        setup_media_dirs()
        setup_afp_connection()

print_django("Finished loading settings.")
