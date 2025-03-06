import re
from typing import Any


def camel_to_snake(name: str) -> str:
    """Convert camelCase string to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def convert_dict_keys(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively convert all dictionary keys from camelCase to snake_case."""
    new_dict = {}
    for key, value in data.items():
        new_key = camel_to_snake(key)
        if isinstance(value, dict):
            new_dict[new_key] = convert_dict_keys(value)
        elif isinstance(value, list):
            new_dict[new_key] = [
                convert_dict_keys(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            new_dict[new_key] = value
    return new_dict


class CamelToSnakeMiddleware:
    """Middleware to convert incoming request data keys from camelCase to snake_case."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Convert POST/PUT/PATCH data
        if hasattr(request, 'data'):
            request.data = convert_dict_keys(request.data)

        # Convert GET parameters
        if request.GET:
            request.GET = request.GET.copy()
            get_params = dict(request.GET.lists())
            converted = convert_dict_keys(get_params)
            request.GET.clear()
            for key, value in converted.items():
                if isinstance(value, list):
                    request.GET.setlist(key, value)
                else:
                    request.GET[key] = value

        response = self.get_response(request)
        return response