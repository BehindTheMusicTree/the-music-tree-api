import json
import logging
import os
import re
from token import NAME


class CONFIG_KEYS:
    class ENV:
        NAME = 'NAME'
        DEBUG = 'DEBUG'
        EXTERNAL_DIRS_NEEDED = 'EXTERNAL_DIRS_NEEDED'
        AUDIO_META_ANALYSE_NEEDED = 'AUDIO_FINGERPRINTER_NEEDED'
        IS_APP_EXPOSED = 'IS_EXPOSED'
        CSRF_TRUSTED_ORIGINS = 'CSRF_TRUSTED_ORIGINS'
        ALLOWED_HOSTS = 'ALLOWED_HOSTS'
        LOG_LEVEL = 'LOG_LEVEL'

    class DEFAULT_INTERNAL_PATHS:
        MEDIA = 'MEDIA'
        LIBRARIES_DIR_NAME = 'LIBRARIES_DIR_NAME'
        TMP_UPLOADED_FILES = 'TMP_UPLOADED_FILES'
        LOG = 'LOG'
        STATIC_FILES = 'STATIC_FILES'


def load_config(config_path='config.json'):
    """Load the configurations from a JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise EnvironmentError(f"The configuration file '{config_path}' was not found.")


CONFIG_WITH_KEYS_IN_CAMEL_CASE = load_config()


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).upper()


def transform_all_keys_from_lower_camel_case_to_capital_snake_case(dictionary):
    return {camel_to_snake(k):
            transform_all_keys_from_lower_camel_case_to_capital_snake_case(v) for k, v in dictionary.items()}


CONFIG = transform_all_keys_from_lower_camel_case_to_capital_snake_case(CONFIG_WITH_KEYS_IN_CAMEL_CASE)

ENVIRONMENTS_CONFIG = CONFIG.get('ENVIRONMENTS', {})

ENV = os.getenv('ENV')
ENV_CONFIG = None
if ENV is None:
    raise EnvironmentError("The ENV variable is not set")
else:
    ENV_CONFIG = ENVIRONMENTS_CONFIG.get(ENV.lower(), {})

    if ENV_CONFIG.get(CONFIG_KEYS.ENV.DEBUG) == True:
        ENV_CONFIG.set(CONFIG_KEYS.ENV.LOG_LEVEL, logging.DEBUG)
    else:
        ENV_CONFIG.set(CONFIG_KEYS.ENV.LOG_LEVEL, logging.INFO)

DEFAULT_INTERNAL_PATHS = CONFIG.get('DEFAULT_INTERNAL_PATHS', {})
