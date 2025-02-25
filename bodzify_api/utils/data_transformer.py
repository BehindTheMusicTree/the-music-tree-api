import re
from typing import Any, Dict, Mapping, Union, cast

from django.http import QueryDict


def remove_substrings_from_string(string_a: str, substrings: list) -> str:
    for substring in substrings:
        string_a = string_a.replace(substring, '')
    return string_a


def convert_data_to_dict(data: Union[QueryDict, Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(data, QueryDict):
        return data.dict()
    elif isinstance(data, Dict):
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
    if isinstance(data, (QueryDict, Dict, Mapping)):
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
    elif isinstance(data, (Dict, Mapping)):
        for key, value in data.items():
            snake_case_key = to_snake_case(key)
            snake_case_dict[snake_case_key] = value

    return snake_case_dict


def get_copy_of_dict_including_only_specified_keys(data_dict: Dict, keys):
    dict2 = data_dict.copy()
    for key in list(dict2.keys()):
        if key not in keys:
            del dict2[key]
    return dict2


def remove_none_or_empty_key_from_dict(data_dict: Dict):
    for key in list(data_dict.keys()):
        if data_dict[key] is None or data_dict[key] == "":
            del data_dict[key]
    return data_dict


def update_dict_converting_str_to_int_value_if_set(key: str, data_dict: Dict):
    if key in data_dict:
        if data_dict[key] is not None and data_dict[key] != '':
            rating = int(data_dict[key])
        else:
            rating = None
        data_dict[key] = rating


def update_dict1_with_key_if_set_in_dict2(key: str, dict1: Dict, dict: Dict):
    if key in dict:
        value = dict[key]
        if value == "":
            value = None
        dict1[key] = value


def override_dict1_with_dict2_values_for_each_key_in_dict2(dict1: Dict, dict2: Dict, keys: list[str]):
    for key in keys:
        update_dict1_with_key_if_set_in_dict2(key=key, dict1=dict1, dict=dict2)


def merge_two_dicts(dict1, dict2):
    dict1.update(dict2)
    return dict1


def replace_none_with_empty_string(**kwargs):
    if kwargs is None:
        return {}
    return {k: ('' if v is None else v) for k, v in kwargs.items()}


def get_first_value_str_if_exists_in_str_dict_or_none(str_dict: Dict, key: str) -> str | None:
    if key in str_dict:
        value = str_dict[key]
        if isinstance(value, list):
            return value[0] if value else None
    else:
        return None


def get_first_value_int_if_exists_in_str_dict_or_none(str_dict: Dict, key: str) -> int | None:
    if key in str_dict:
        value = str_dict[key]
        if isinstance(value, list):
            value_str = value[0] if value else ""
        else:
            value_str = str(value)

        if value_str and value_str.strip():
            try:
                return int(value_str)
            except ValueError:
                return None
    return None
