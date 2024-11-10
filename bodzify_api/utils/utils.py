import random
import string
from typing import Any, Dict, Union

from django.http import QueryDict


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def print_django(message):
    print(f"[Django] {message}")


def remove_substrings_from_string(string_a: str, substrings: list) -> str:
    for substring in substrings:
        string_a = string_a.replace(substring, '')
    return string_a


def convert_data_to_dict(data: Union[QueryDict, Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(data, QueryDict):
        return data.dict()
    elif isinstance(data, dict):
        return data
    else:
        return {k: v for k, v in data.items()}


def generate_short_uu(length: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_substring_after_last_slash(string: str):
    return string.split("/")[-1]


def get_file_extension_from_url(url: str):
    return url.split(".")[-1]


def get_copy_of_dict_including_only_specified_keys(dict: Dict, keys):
    dict2 = dict.copy()
    for key in list(dict2.keys()):
        if key not in keys:
            del dict2[key]
    return dict2


def remove_none_or_empty_key_from_dict(dict: Dict):
    for key in list(dict.keys()):
        if dict[key] is None or dict[key] == "":
            del dict[key]
    return dict


def update_data1_converting_str_to_int_value_if_set(key: str, data1: dict):
    if key in data1:
        if data1[key] and data1[key] != '':
            rating = int(data1[key])
        else:
            rating = None
        data1[key] = rating


def update_data1_with_key_if_set_in_data2(key: str, data1: dict, data2: dict):
    if key in data2:
        value = data2[key]
        if value == "":
            value = None
        data1[key] = value


def override_data1_with_data2_values_for_each_key_in_data2(data1: dict, data2: dict, keys: list[str]):
    for key in keys:
        update_data1_with_key_if_set_in_data2(key=key, data1=data1, data2=data2)
