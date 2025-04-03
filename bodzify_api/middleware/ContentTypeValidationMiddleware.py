from typing import Union

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from rest_framework.request import Request

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class ContentTypeValidationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def handle_error(self, exc: Union[ParseError, UnsupportedMediaType]) -> JsonResponse:
        """Handle middleware errors by converting them to proper error responses."""
        return ErrorResponse.handle_exception(exc)

    def __call__(self, request: Union[HttpRequest, Request]) -> Union[HttpResponse, JsonResponse]:
        if request.method in ['POST', 'PUT', 'PATCH']:
            # Check for test flag to simulate missing content type
            # This allows tests to force a missing content type scenario
            force_empty_content_type = request.META.get('HTTP_X_TEST_FORCE_EMPTY_CONTENT_TYPE') == 'true'

            # Use the real content type unless we're forcing an empty one for testing
            content_type = '' if force_empty_content_type else (request.content_type or '')

            if not content_type:
                return self.handle_error(UnsupportedMediaType('Content-Type header is required'))

            if content_type not in ['application/json', 'multipart/form-data', 'application/x-www-form-urlencoded']:
                return self.handle_error(UnsupportedMediaType(
                    'Unsupported content type. Use application/json for regular requests or '
                    'multipart/form-data for file uploads'))

            # Validate JSON content
            if content_type == 'application/json' and request.body:
                try:
                    decoded = request.body.decode('utf-8').strip()
                    # Reject if it looks like a JSON string (double-encoded)
                    if decoded.startswith('"') and decoded.endswith('"'):
                        return self.handle_error(ParseError(
                            'Double-encoded JSON detected. Send the JSON object directly without string encoding.'))
                except UnicodeDecodeError:
                    return self.handle_error(ParseError('Invalid UTF-8 encoding'))

        return self.get_response(request)
