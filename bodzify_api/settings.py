#!/usr/bin/env python

import datetime
import os
from pathlib import Path
import subprocess
import sys
import dotenv


def print_django(message):
    print(f"[Django] {message}")


def remove_eventual_surronding_quotes(s: str) -> str:
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def load_calculated_env_paths():
    CALCULATED_PATHS_ENV_FILE = BASE_DIR / 'env/calculated_paths/.env'
    generate_calculated_paths_env_file_script_path = BASE_DIR / 'scripts/generate_calculated_paths_env_file.sh'
    try:
        result = subprocess.run(['bash', str(generate_calculated_paths_env_file_script_path)],
                                check=True,
                                stderr=subprocess.PIPE,
                                text=True,
                                env=os.environ.copy())
    except subprocess.CalledProcessError as e:
        print_django("Error while generating the paths env file:", e.stderr)  # type: ignore
        raise EnvironmentError("Error while generating the paths env file: " + str(e)) from e

    dotenv.load_dotenv(CALCULATED_PATHS_ENV_FILE)


def load_env_vars_from_file():
    APP_ENV_FILE_RELATIVE_PATH = os.getenv('ENV_FILE', 'env/.env')
    APP_ENV_FILE = BASE_DIR / APP_ENV_FILE_RELATIVE_PATH
    if not APP_ENV_FILE.exists():
        print_django(f"No env file at {APP_ENV_FILE}")
        APP_ENV_FILE = None
    else:
        print_django(f"Env file provided at {APP_ENV_FILE} . Loading...")
        dotenv.load_dotenv(APP_ENV_FILE)
        print_django("Env file loaded.")


def init_logs_if_needed():
    LOG_DIR_STR = os.getenv('DJANGO_LOG_DIR')
    if not LOG_DIR_STR:
        print_django("The DJANGO_LOG_DIR variable is not set. Logs will not be set up.")
    else:
        print_django("LOG_DIR is set. Setting up logs...")

        LOG_DIR = Path(LOG_DIR_STR)
        if not LOG_DIR.exists():
            raise EnvironmentError(f"The log directory {LOG_DIR} does not exist.")
        print_django(f"The log dir {LOG_DIR} exists.")

        LOG_GENERAL_FILENAME = os.getenv('DJANGO_LOG_GENERAL_FILENAME')
        if not LOG_GENERAL_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_GENERAL_FILENAME variable must be set")
        LOG_GENERAL_FILE = LOG_DIR / LOG_GENERAL_FILENAME
        if not LOG_GENERAL_FILE.exists():
            raise EnvironmentError(f"The log general file {LOG_GENERAL_FILE} does not exist.")
        print_django("The log general file {LOG_GENERAL_FILE} exists.")

        LOG_INFO_FILENAME = os.getenv('DJANGO_LOG_INFO_FILENAME')
        if not LOG_INFO_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_INFO_FILENAME variable must be set")
        LOG_INFO_FILE = LOG_DIR / LOG_INFO_FILENAME
        if not LOG_INFO_FILE.exists():
            raise EnvironmentError(f"The log info file {LOG_INFO_FILE} does not exist.")
        print_django(f"The log info file {LOG_INFO_FILE} exists.")

        LOG_REQUESTS_FILENAME = os.getenv('DJANGO_LOG_REQUESTS_FILENAME')
        if not LOG_REQUESTS_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_REQUESTS_FILENAME variable must be set")
        LOG_REQUESTS_FILE = LOG_DIR / LOG_REQUESTS_FILENAME
        if not LOG_REQUESTS_FILE.exists():
            raise EnvironmentError(f"The log requests file {LOG_REQUESTS_FILE} does not exist.")
        print_django(f"The log info file {LOG_REQUESTS_FILE} exists.")

        LOG_REQUESTS_DEBUG_FILENAME = os.getenv('DJANGO_LOG_REQUESTS_DEBUG_FILENAME')
        if not LOG_REQUESTS_DEBUG_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_REQUESTS_DEBUG_FILENAME variable must be set")
        LOG_REQUESTS_DEBUG_FILE = LOG_DIR / LOG_REQUESTS_DEBUG_FILENAME
        if not LOG_REQUESTS_DEBUG_FILE.exists():
            raise EnvironmentError(f"The log requests debug file {LOG_REQUESTS_DEBUG_FILE} does not exist.")
        print_django(f"The log info file {LOG_REQUESTS_DEBUG_FILE} exists.")

        LOG_EXCEPTIONS_FILENAME = os.getenv('DJANGO_LOG_EXCEPTIONS_FILENAME')
        if not LOG_EXCEPTIONS_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_EXCEPTIONS_FILENAME variable must be set")
        LOG_EXCEPTIONS_FILE = LOG_DIR / LOG_EXCEPTIONS_FILENAME
        if not LOG_EXCEPTIONS_FILE.exists():
            raise EnvironmentError(f"The log exceptions file {LOG_EXCEPTIONS_FILE} does not exist.")
        print_django(f"The log info file {LOG_EXCEPTIONS_FILE} exists.")

        LOG_DJANGO_FILENAME = os.getenv('DJANGO_LOG_DJANGO_FILENAME')
        if not LOG_DJANGO_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_DJANGO_FILENAME variable must be set")
        LOG_DJANGO_FILE = LOG_DIR / LOG_DJANGO_FILENAME
        if not LOG_DJANGO_FILE.exists():
            raise EnvironmentError(f"The log django file {LOG_DJANGO_FILE} does not exist.")
        print_django(f"The log info file {LOG_DJANGO_FILE} exists.")

        LOG_APP_FILENAME = os.getenv('DJANGO_LOG_APP_FILENAME')
        if not LOG_APP_FILENAME:
            raise EnvironmentError("The DJANGO_LOG_APP_FILENAME variable must be set")
        LOG_APP_FILE = LOG_DIR / LOG_APP_FILENAME
        if not LOG_APP_FILE.exists():
            raise EnvironmentError(f"The log app file {LOG_APP_FILE} does not exist.")
        print_django(f"The log info file {LOG_APP_FILE} exists.")

        global LOGGING
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
        print_django("Logs are set up.")


def setup_app_exposure_if_needed():
    global ALLOWED_HOSTS
    global SECRET_KEY

    APP_VERSION = os.getenv('APP_VERSION')
    if not APP_VERSION:
        raise EnvironmentError("The APP_VERSION variable must be set")
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

        CSRF_TRUSTED_ORIGINS_STR = os.getenv('CSRF_TRUSTED_ORIGINS')
        if not CSRF_TRUSTED_ORIGINS_STR:
            raise EnvironmentError("The CSRF_TRUSTED_ORIGINS variable must be set")
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

        ALLOWED_HOSTS_STR = os.getenv('ALLOWED_HOSTS')
        if not ALLOWED_HOSTS_STR:
            raise EnvironmentError("The ALLOWED_HOSTS variable must be set")
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

        # SECURITY WARNING: keep the secret key used in production secret!
        SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
        if not SECRET_KEY:
            raise EnvironmentError("The DJANGO_SECRET_KEY variable must be set")
    else:
        ALLOWED_HOSTS = ['127.0.0.1']
        SECRET_KEY = "django-default-secret-when-not-exposed"

    print_django("The secret key is set.")
    print_django(f"ALLOWED_HOSTS is set to {ALLOWED_HOSTS}")
    global CORS_ALLOW_ALL_ORIGINS
    CORS_ALLOW_ALL_ORIGINS = True  # TODO: don't allow all
    print_django(f"CORS_ALLOW_ALL_ORIGINS is set to: {CORS_ALLOW_ALL_ORIGINS}")


BASE_DIR = Path(__file__).resolve().parent.parent


def setup_app_constants():
    # Before calling a view function, Django starts a transaction.
    # If the response is produced without problems, Django commits the transaction.
    # If the view produces an exception, Django rolls back the transaction.
    global ATOMIC_REQUESTS
    ATOMIC_REQUESTS = True

    # SECURITY WARNING: don't run with debug turned on in production!
    global DEBUG
    DEBUG = os.getenv('DEBUG')
    if not DEBUG or DEBUG not in ['true', 'false']:
        raise EnvironmentError("The DEBUG variable is not set or is not a boolean")

    global UUID_LEN
    UUID_LEN = 22

    global USER_LIBRARIES_DIR_NAME_PREFIXE
    USER_LIBRARIES_DIR_NAME_PREFIXE = "user_"
    global USER_MAX_NUMBER
    USER_MAX_NUMBER = "10000000"  # hehe

    global FILE_PATH_MAX_LENGTH
    FILE_PATH_MAX_LENGTH = 255
    global LIB_TRACK_FILE_SIZE_MIN_IN_MO
    LIB_TRACK_FILE_SIZE_MIN_IN_MO = 0
    global LIB_TRACK_FILE_SIZE_MAX_IN_MO
    LIB_TRACK_FILE_SIZE_MAX_IN_MO = 300
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
    global ALBUM_ARTISTS_FIELD_LEN_MAX
    ALBUM_ARTISTS_FIELD_LEN_MAX = 200
    global ARTIST_NAME_LEN_MAX
    ARTIST_NAME_LEN_MAX = 200
    global CRITERIA_NAME_LEN_MAX
    CRITERIA_NAME_LEN_MAX = 200
    global SIMPLE_PLAYLIST_NAME_LEN_MAX
    SIMPLE_PLAYLIST_NAME_LEN_MAX = 200

    MUSICBRAINZ_BASE_URL = "https://musicbrainz.org/"
    global MUSICBRAINZ_RECORDING_URL
    MUSICBRAINZ_RECORDING_URL = MUSICBRAINZ_BASE_URL + "recording/"
    global MUSICBRAINZ_RECORDING_TITLE_LEN_MAX
    MUSICBRAINZ_RECORDING_TITLE_LEN_MAX = 200
    global MUSICBRAINZ_LOOKUP_ERROR_STR_LEN_MAX
    MUSICBRAINZ_LOOKUP_ERROR_STR_LEN_MAX = 255
    global MUSICBRAINZ_ARTIST_URL
    MUSICBRAINZ_ARTIST_URL = MUSICBRAINZ_BASE_URL + "artist/"
    global MUSICBRAINZ_ARTIST_NAME_LEN_MAX
    MUSICBRAINZ_ARTIST_NAME_LEN_MAX = 200

    global PAGINATION_LIMIT_OFFSET_DEFAULT
    PAGINATION_LIMIT_OFFSET_DEFAULT = 30


def setup_afp_connection():
    global AFP_BASE_URL
    AFP_BASE_URL = "http://127.0.0.1"


def setup_static_files_if_needed():
    global STATIC_FILES
    STATIC_FILES = os.getenv('STATIC_FILES')
    if not STATIC_FILES:
        print_django("Static files are not needed.")
        static_files_are_being_served_or_collected = False
    else:
        print_django("STATIC_FILES is set. Setting up static files configuration...")
        static_files_are_being_served_or_collected = True

        if ENV == 'COLLECT_STATIC' or APP_IS_EXPOSED is False:
            print_django("The app is in collect static mode or is not exposed (which means no web server). STATIC_ROOT is needed.")
            global STATIC_ROOT
            STATIC_ROOT = Path(STATIC_FILES)
            print_django("STATIC_ROOT: " + str(STATIC_ROOT))
            if not STATIC_ROOT.exists():
                raise EnvironmentError(f"The static root {STATIC_ROOT} does not exist.")
            print_django(f"{STATIC_ROOT} exists.")
        else:
            print_django(
                "The app is exposed (which means it has a web server) or is not in collect static mode. STATIC_ROOT is \
                not needed.")
        global STATIC_URL
        STATIC_URL = '/static/'
        # STATICFILES_DIRS = [] # No additional static files directories are needed.

    return static_files_are_being_served_or_collected


def setup_installed_apps(static_files_are_being_served_or_collected: bool, app_is_exposed: bool):
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

    if app_is_exposed:
        INSTALLED_APPS.append('rest_framework_simplejwt')

    if static_files_are_being_served_or_collected:
        INSTALLED_APPS.append('django.contrib.staticfiles')


def setup_middlewares():
    global MIDDLEWARE
    MIDDLEWARE = [f'{APP_NAME}.middleware.ExceptionLoggingMiddleware.ExceptionLoggingMiddleware',
                  f'{APP_NAME}.middleware.RequestLoggingMiddleware.RequestLoggingMiddleware',
                  'django.middleware.security.SecurityMiddleware',
                  'corsheaders.middleware.CorsMiddleware',
                  'django.contrib.sessions.middleware.SessionMiddleware',
                  'django.middleware.common.CommonMiddleware',
                  'django.middleware.csrf.CsrfViewMiddleware',
                  'django.contrib.auth.middleware.AuthenticationMiddleware',
                  'django.contrib.messages.middleware.MessageMiddleware',
                  'django.middleware.clickjacking.XFrameOptionsMiddleware']


def setup_db_connection_if_needed():
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

        DB_BODZIFY_API_USER_PASSWORD_WITH_EVENTUAL_QUOTES = os.getenv('DB_BODZIFY_API_USER_PASSWORD')
        if DB_BODZIFY_API_USER_PASSWORD_WITH_EVENTUAL_QUOTES is None:
            raise EnvironmentError("The DB_BODZIFY_API_USER_PASSWORD variable must be set")
        DB_BODZIFY_API_USER_PASSWORD = remove_eventual_surronding_quotes(
            DB_BODZIFY_API_USER_PASSWORD_WITH_EVENTUAL_QUOTES)

        if APP_IS_EXPOSED:
            print_django("The app is exposed. The db host is the db container name.")
            DB_CONTAINER_NAME = os.getenv('DB_CONTAINER_NAME')
            if not DB_CONTAINER_NAME:
                raise EnvironmentError("The DB_CONTAINER_NAME variable must be set")
            DB_HOST = DB_CONTAINER_NAME
        else:
            print_django("The app is not exposed. The db host is the db url.")
            DB_URL = os.getenv('DB_URL')
            if DB_URL is None:
                raise EnvironmentError("The DB_URL variable must be set")
            DB_HOST = DB_URL
        print_django("DB_HOST: " + DB_HOST)

        DB_PORT = os.getenv('DB_PORT')
        if DB_PORT is None:
            raise EnvironmentError("The DB_PORT variable must be set")

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


def setup_media_dirs_if_needed():
    global FILE_UPLOAD_ENABLED
    TMP_UPLOADED_FILES_STR = os.getenv('TMP_UPLOADED_FILES')
    if not TMP_UPLOADED_FILES_STR:
        print_django("TMP_UPLOADED_FILES is not set. The app will not handle media files.")
        FILE_UPLOAD_ENABLED = False

        for var_name in ['AFP_PORT',
                         'AFP_POST_ENDPOINT',
                         'ACOUSTID_API_KEY',
                         'MEDIA_DIR',
                         'LIBRARIES_DIR_NAME']:
            if os.getenv(var_name):
                raise EnvironmentError(f"The {var_name} env variable cannot be set as TMP_UPLOADED_FILES is not.")
    else:
        print_django("TMP_UPLOADED_FILES is set. Setting up the media variables...")
        FILE_UPLOAD_ENABLED = True
        global AFP_CONTAINER_NAME
        AFP_CONTAINER_NAME = os.getenv('AFP_CONTAINER_NAME')
        if not AFP_CONTAINER_NAME:
            raise EnvironmentError("The AFP_CONTAINER_NAME variable must be set")

        TMP_UPLOADED_FILES_DIR_ENV = os.getenv('TMP_UPLOADED_FILES')
        if not TMP_UPLOADED_FILES_DIR_ENV:
            raise EnvironmentError("The TMP_UPLOADED_FILES variable must be set")
        global FILE_UPLOAD_TEMP_DIR
        FILE_UPLOAD_TEMP_DIR = Path(TMP_UPLOADED_FILES_DIR_ENV)  # Django constant, do not rename.
        print_django("FILE_UPLOAD_TEMP_DIR: " + str(FILE_UPLOAD_TEMP_DIR))
        if not FILE_UPLOAD_TEMP_DIR.exists():
            raise EnvironmentError(f"The file upload temp directory {FILE_UPLOAD_TEMP_DIR} does not exist.")
        print_django("The FILE_UPLOAD_TEMP_DIR directory exists.")

        global AFP_PORT
        AFP_PORT = os.getenv('AFP_PORT')
        if AFP_PORT is None:
            raise Exception("AFP_PORT env variable must be set")

        AFP_POST_ENDPOINT = os.getenv('AFP_POST_ENDPOINT')
        if AFP_POST_ENDPOINT is None:
            raise Exception("AFP_POST_ENDPOINT env variable must be set")

        global AFP_POST_FULL_URL
        AFP_POST_FULL_URL = AFP_BASE_URL + ":" + AFP_PORT + '/' + AFP_POST_ENDPOINT

        global ACOUSTID_API_KEY
        ACOUSTID_API_KEY = os.getenv('ACOUSTID_API_KEY')
        if not ACOUSTID_API_KEY and FILE_UPLOAD_ENABLED:
            raise EnvironmentError("The ACOUSTID_API_KEY variable must be set")

        MEDIA_DIR_ENV = os.getenv('MEDIA_DIR')
        if not MEDIA_DIR_ENV:
            raise EnvironmentError("The MEDIA_DIR variable must be set")
        global MEDIA_ROOT
        MEDIA_ROOT = Path(MEDIA_DIR_ENV)  # Django constant, do not rename.
        print_django("MEDIA_ROOT: " + str(MEDIA_ROOT))
        if not MEDIA_ROOT.exists():
            raise EnvironmentError(f"The media root directory {MEDIA_ROOT} does not exist.")
        print_django("The MEDIA_ROOT directory exists.")

        global LIBRARIES_DIR_NAME
        LIBRARIES_DIR_NAME = os.getenv('LIBRARIES_DIR_NAME')
        if not LIBRARIES_DIR_NAME:
            raise EnvironmentError("The LIBRARIES_DIR_NAME variable must be set")

        global LIBRARIES_DIR
        LIBRARIES_DIR = MEDIA_ROOT / LIBRARIES_DIR_NAME
        print_django("LIBRARIES_DIR: " + str(LIBRARIES_DIR))
        if not LIBRARIES_DIR.exists():
            raise EnvironmentError(f"The libraries directory {LIBRARIES_DIR} does not exist.")
        print_django("The LIBRARIES_DIR directory exists.")
        print_django("Media variables are set.")


load_env_vars_from_file()

ENV = os.getenv('ENV')
if not ENV:
    raise EnvironmentError("The ENV variable must be set")
print_django(f"ENV is set to {ENV}")

APP_NAME = os.getenv('APP_NAME')
if not APP_NAME:
    raise EnvironmentError("The APP_NAME variable must be set")

APP_IS_EXPOSED_STR = os.getenv('APP_IS_EXPOSED')
if not APP_IS_EXPOSED_STR:
    raise EnvironmentError("The APP_IS_EXPOSED variable must be set")
APP_IS_EXPOSED_STR = APP_IS_EXPOSED_STR.lower()
if APP_IS_EXPOSED_STR not in ['true', 'false']:
    raise EnvironmentError("The APP_IS_EXPOSED variable is not a boolean")

APP_IS_EXPOSED = (APP_IS_EXPOSED_STR == 'true')
FILE_UPLOAD_ENABLED = None

if 'loaddata' in sys.argv:
    print_django("settings.py is being executed because of a loaddata command.")
    setup_app_constants()
    setup_installed_apps(static_files_are_being_served_or_collected=False,
                         app_is_exposed=False)
    setup_middlewares()
    setup_django_constants()
    setup_db_connection_if_needed()
    setup_templates()  # Needed to use the admin application
else:
    print_django("settings.py is not being executed because of a loaddata command.")
    load_calculated_env_paths()
    setup_app_exposure_if_needed()
    setup_app_constants()
    setup_afp_connection()
    static_files_are_being_served_or_collected = setup_static_files_if_needed()
    setup_installed_apps(static_files_are_being_served_or_collected=static_files_are_being_served_or_collected,
                         app_is_exposed=APP_IS_EXPOSED)
    setup_middlewares()
    setup_db_connection_if_needed()
    setup_templates()
    setup_django_constants()
    setup_media_dirs_if_needed()
    init_logs_if_needed()

print_django("Finished loading settings.")
