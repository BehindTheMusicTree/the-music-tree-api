
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


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

    def __init__(self, get_response):
        self.get_response = get_response

    def _handle_duplicate_field_error_for_content_type_json(self, field_name: str) -> JsonResponse:
        # raise_validation_error always raises an exception, so this will always go to the except block
        raise_validation_error(
            message='Duplicate field detected.',
            field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT,
            field=field_name
        )
        # This is unreachable but makes the type checker happy
        raise RuntimeError('Unreachable - raise_validation_error always raises')

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type or ''
            # Only check for duplicates in JSON data
            # Multipart/form-data allows multiple fields with the same name by design
            if content_type == 'application/json':
                try:
                    raw_body = request.body.decode('utf-8')
                    duplicate_fields = find_duplicate_fields(raw_body)
                    if duplicate_fields:
                        return self._handle_duplicate_field_error_for_content_type_json(duplicate_fields[0])
                except UnicodeDecodeError:
                    # Let system errors propagate up to be handled by global error handler
                    raise

        return self.get_response(request)
