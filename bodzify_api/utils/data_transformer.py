import re
from typing import Dict, Any, Union, cast, Mapping

from django.http import QueryDict


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


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def to_dict(data: Any) -> Union[QueryDict, Dict[str, Any], Mapping[str, Any]]:
    if isinstance(data, (QueryDict, dict, Mapping)):
        return cast(Union[QueryDict, Dict[str, Any], Mapping[str, Any]], data)
    return dict(data)


def dict_to_snake_case(data: Any) -> Dict[str, Any]:
    data_dict = to_dict(data)
    return {to_snake_case(key): value for key, value in data_dict.items()}


def form_data_to_snake_case(form_data: Any) -> Dict[str, Any]:
    data = to_dict(form_data)
    snake_case_dict: Dict[str, Any] = {}

    if isinstance(data, QueryDict):
        for key, values in data.lists():
            snake_case_key = to_snake_case(key)
            snake_case_dict[snake_case_key] = values[0] if len(values) == 1 else values
    elif isinstance(data, (dict, Mapping)):
        for key, value in data.items():
            snake_case_key = to_snake_case(key)
            snake_case_dict[snake_case_key] = value

    return snake_case_dict


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


def update_dict_converting_str_to_int_value_if_set(key: str, data_dict: dict):
    if key in data_dict:
        if data_dict[key] is not None and data_dict[key] != '':
            rating = int(data_dict[key])
        else:
            rating = None
        data_dict[key] = rating


def update_data1_with_key_if_set_in_data2(key: str, data1: dict, data2: dict):
    if key in data2:
        value = data2[key]
        if value == "":
            value = None
        data1[key] = value


def override_data1_with_data2_values_for_each_key_in_data2(data1: dict, data2: dict, keys: list[str]):
    for key in keys:
        update_data1_with_key_if_set_in_data2(key=key, data1=data1, data2=data2)


def merge_two_dicts(dict1, dict2):
    dict1.update(dict2)
    return dict1


def replace_none_with_empty_string(**kwargs):
    if kwargs is None:
        return {}
    return {k: ('' if v is None else v) for k, v in kwargs.items()}
