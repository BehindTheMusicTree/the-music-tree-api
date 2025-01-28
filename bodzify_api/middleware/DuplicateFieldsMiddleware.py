
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.exceptions import ValidationError
from bodzify_api.view.error.ErrorResponse import ErrorResponse


def find_duplicate_fields(json_str: str) -> list[str]:
    """Find duplicate fields in a JSON string."""
    try:
        decoder = json.JSONDecoder()
        pos = 0
        fields = []

        while pos < len(json_str):
            # Skip whitespace
            while pos < len(json_str) and json_str[pos].isspace():
                pos += 1
            if pos >= len(json_str):
                break

            # If we find a field name (starts with ")
            if json_str[pos] == '"':
                end = json_str.find('"', pos + 1)
                if end != -1:
                    field = json_str[pos + 1:end]
                    if field in fields:
                        return [field]  # Found a duplicate
                    fields.append(field)
                    pos = end + 1
            else:
                pos += 1

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
