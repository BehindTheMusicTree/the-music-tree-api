from typing import Union

from django.http import HttpRequest, HttpResponse
from rest_framework.exceptions import ParseError, UnsupportedMediaType
from rest_framework.request import Request


class ContentTypeValidationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Union[HttpRequest, Request]) -> HttpResponse:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request  .content_type or ''

            if not content_type:
                raise UnsupportedMediaType('Content-Type header is required')

            if content_type not in ['application/json', 'multipart/form-data']:
                raise UnsupportedMediaType('Unsupported content type. Use application/json for regular requests or '
                                           'multipart/form-data for file uploads')

            # Validate JSON content
            if content_type == 'application/json' and request.body:
                try:
                    decoded = request.body.decode('utf-8').strip()
                    # Reject if it looks like a JSON string (double-encoded)
                    if decoded.startswith('"') and decoded.endswith('"'):
                        raise ParseError(
                            'Double-encoded JSON detected. Send the JSON object directly without string encoding.')
                except UnicodeDecodeError:
                    raise ParseError('Invalid UTF-8 encoding')

        return self.get_response(request)
