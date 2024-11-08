import re
from typing import Dict, Any, Union, cast, Mapping

from django.http import QueryDict


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
