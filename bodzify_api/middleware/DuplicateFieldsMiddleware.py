
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.exceptions import ValidationError
from bodzify_api.view.error.ErrorResponse import ErrorResponse


def find_duplicate_fields(json_str: str) -> list[str]:
    """Find duplicate fields in a JSON object, only considering field names at the same level."""
    try:
        # Parse the JSON string into a Python object
        data = json.loads(json_str)

        def check_dict_duplicates(obj: dict) -> list[str]:
            # Convert keys to list to check for duplicates in raw JSON
            keys_list = list(obj.keys())
            # If the number of unique keys is less than total keys, we have duplicates
            if len(set(keys_list)) < len(keys_list):
                # Find the first duplicate key
                seen = set()
                for key in keys_list:
                    if key in seen:
                        return [key]
                    seen.add(key)

            # Recursively check nested dictionaries
            for value in obj.values():
                if isinstance(value, dict):
                    result = check_dict_duplicates(value)
                    if result:
                        return result
            return []

        # Only check for duplicates if the root is a dictionary
        if isinstance(data, dict):
            return check_dict_duplicates(data)
        return []
    except json.JSONDecodeError:
        return []


class DuplicateFieldsMiddleware:
    """Middleware to preserve raw request body for duplicate field detection."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                raw_body = request.body.decode('utf-8')
                duplicate_fields = find_duplicate_fields(raw_body)
                if duplicate_fields:
                    validation_error = ValidationError({
                        'duplicate_fields': {
                            'code': 'duplicate_fields',
                            'field': duplicate_fields[0]  # Show the field name that has duplicates
                        }
                    })
                    error_response = ErrorResponse.from_validation_error(validation_error)
                    return JsonResponse(
                        error_response.data,
                        status=error_response.status_code,
                        content_type='application/json'
                    )
            except UnicodeDecodeError:
                pass

        return self.get_response(request)
