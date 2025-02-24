import json
from typing import Union

from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationError import AppValidationError
from bodzify_api.view.error.ErrorResponse import ErrorResponse

from .JsonDuplicateKeyDetectingDecoder import JsonDuplicateKeyDetectingDecoder


class DuplicateFieldsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def find_duplicate_fields_in_json(self, json_str: str) -> list[str]:
        try:
            decoder = JsonDuplicateKeyDetectingDecoder()
            decoder.decode(json_str)
            return decoder.tracker.duplicates
        except json.JSONDecodeError:
            return []

    def _handle_duplicate_field_error_for_content_type_json(self, field_name: str) -> HttpResponse:
        validation_error = AppValidationError(
            field_name=field_name,
            message='Duplicate field detected.',
            field_validation_error_code=FieldValidationErrorCode.FIELD_DUPLICATE
        )
        return ErrorResponse.from_validation_error(validation_error)

    def __call__(self, request: Union[HttpRequest, Request]) -> HttpResponse:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type or ''

            if content_type == 'application/json':
                try:
                    raw_body = request.body.decode('utf-8')
                    duplicate_fields = self.find_duplicate_fields_in_json(raw_body)
                    if duplicate_fields:
                        return self._handle_duplicate_field_error_for_content_type_json(duplicate_fields[0])
                except UnicodeDecodeError:
                    # Let system errors propagate up to be handled by global error handler
                    raise
            elif content_type.startswith('multipart/form-data'):
                # For multipart requests, data can be in POST (for POST) or data (for PUT/PATCH)
                # Django REST framework puts all data in request.data
                if isinstance(request, Request):
                    data = request.data  # type: Any
                else:
                    # Fallback to POST if request.data is not available
                    data = request.POST

                seen_fields = {}
                duplicates = []

                # Check for duplicates while allowing list fields
                for field_name in data.keys():
                    # Skip list fields (fields that appear multiple times)
                    if hasattr(data, 'getlist'):  # Handle QueryDict
                        values = data.getlist(field_name)
                        has_multiple_values = len(values) > 1
                    else:  # Handle regular Dict
                        value = data.get(field_name)
                        has_multiple_values = isinstance(value, (list, tuple))

                    if has_multiple_values:
                        continue

                    if field_name in seen_fields:
                        duplicates.append(field_name)
                    else:
                        seen_fields[field_name] = True

                if duplicates:
                    return self._handle_duplicate_field_error_for_content_type_json(duplicates[0])

        return self.get_response(request)
