import json
import logging
import os
import re
from token import NAME

DEFAULT_INTERNAL_PATHS_CONFIG_FILE = 'default_internal_paths_config.json'


class CONFIG_KEYS:
    MEDIA = 'MEDIA'
    LIBRARIES_DIR_NAME = 'LIBRARIES_DIR_NAME'
    TMP_UPLOADED_FILES = 'TMP_UPLOADED_FILES'
    LOG = 'LOG'
    STATIC_FILES = 'STATIC_FILES'


def load_config(config_path=DEFAULT_INTERNAL_PATHS_CONFIG_FILE):
    """Load the configurations from a JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise EnvironmentError(f"The configuration file '{config_path}' was not found.")


def transform_all_keys_from_lower_camel_case_to_capital_snake_case(dictionary):
    if isinstance(dictionary, dict):
        return {
            transform_key_from_lower_camel_case_to_capital_snake_case(k):
            transform_all_keys_from_lower_camel_case_to_capital_snake_case(v) for k, v in dictionary.items()
        }
    elif isinstance(dictionary, list):
        return [transform_all_keys_from_lower_camel_case_to_capital_snake_case(item) for item in dictionary]
    else:
        return dictionary


def transform_key_from_lower_camel_case_to_capital_snake_case(key):
    key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).upper()


def load() -> dict:
    DEFAULT_INTERNAL_PATHS_WITH_KEYS_IN_CAMEL_CASE = load_config()
    return transform_all_keys_from_lower_camel_case_to_capital_snake_case(
        DEFAULT_INTERNAL_PATHS_WITH_KEYS_IN_CAMEL_CASE)
