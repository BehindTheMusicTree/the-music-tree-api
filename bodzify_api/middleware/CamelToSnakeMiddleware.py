
import json
from json.decoder import JSONDecodeError
from typing import Any, Mapping, cast

from django.http import QueryDict
from rest_framework.request import Request

from bodzify_api.utils import data_transformer


class CamelToSnakeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        content_type = request.headers.get('Content-Type', '')

        if content_type.startswith('application/json'):
            try:
                if request.body:
                    json_data = cast(dict, json.loads(request.body))
                    request.data = self._form_data_to_snake_case(json_data)  # type: ignore
                else:
                    request.data = {}  # type: ignore
            except JSONDecodeError:
                request.data = {}  # type: ignore

        if content_type.startswith('multipart/form-data'):
            request.POST = self._form_data_to_snake_case(request.POST)  # type: ignore

            if request.FILES:
                original_files = request.FILES
                request._files = dict()  # type: ignore
                for key, files in original_files.items():
                    request._files[data_transformer.to_snake_case(key)] = files

        # Convert GET parameters
        if request.GET:
            request.GET = request.GET.copy()
            get_params = dict(request.GET.lists())
            converted = data_transformer.dict_to_snake_case(get_params)
            request.GET.clear()
            for key, value in converted.items():
                if isinstance(value, list):
                    request.GET.setlist(key, value)
                else:
                    request.GET[key] = value

        response = self.get_response(request)
        return response

    def _form_data_to_snake_case(self, form_data: Any) -> dict[str, Any]:
        data = data_transformer.to_dict(form_data)
        snake_case_dict: dict[str, Any] = {}

        if isinstance(data, QueryDict):
            for key, values in data.lists():
                snake_case_key = data_transformer.to_snake_case(key)
                snake_case_dict[snake_case_key] = values[0] if len(values) == 1 else values
        elif isinstance(data, (dict, Mapping)):
            for key, value in data.items():
                snake_case_key = data_transformer.to_snake_case(key)
                snake_case_dict[snake_case_key] = value

        return snake_case_dict
