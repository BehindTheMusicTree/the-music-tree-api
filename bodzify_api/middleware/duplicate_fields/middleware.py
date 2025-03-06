import json
from typing import Any, Union

from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
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

    def __call__(self, request: Union[HttpRequest, Request]) -> HttpResponse:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type or ''

            if content_type == 'application/json':
                try:
                    raw_body = request.body.decode('utf-8')
                    duplicate_fields = self.find_duplicate_fields_in_json(raw_body)
                    if duplicate_fields:
                        # Raise the validation exception to be handled by ExceptionLoggingMiddleware
                        raise AppValidationException(
                            field_name=duplicate_fields[0],
                            message='Duplicate field detected.',
                            field_validation_error_code=FieldValidationErrorCode.DUPLICATE
                        )
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
                    if hasattr(data, 'getList'):  # Handle QueryDict
                        values = data.getList(field_name)
                        has_multiple_values = len(values) > 1
                    else:  # Handle regular dict
                        value = data.get(field_name)
                        has_multiple_values = isinstance(value, (list, tuple))

                    if has_multiple_values:
                        continue

                    if field_name in seen_fields:
                        duplicates.append(field_name)
                    else:
                        seen_fields[field_name] = True

                if duplicates:
                    # Raise the validation exception to be handled by ExceptionLoggingMiddleware
                    raise AppValidationException(
                        field_name=duplicates[0],
                        message='Duplicate field detected.',
                        field_validation_error_code=FieldValidationErrorCode.DUPLICATE
                    )

        return self.get_response(request)
