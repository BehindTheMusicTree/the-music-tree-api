import logging
from typing import Union

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.exceptions import ParseError
from rest_framework.request import Request

from bodzify_api.view.error.ErrorResponse import ErrorResponse

logger = logging.getLogger(__name__)


class ContentValidityMiddleware:
    """
    Middleware to validate that request data is accessible and properly parsed.

    This middleware ensures that after CamelToSnakeMiddleware processes the request,
    request.data is accessible and valid. If accessing request.data raises an exception,
    this indicates a structural problem (corrupted data, parsing failure, etc.) and the
    request is rejected.

    Implementation:
    ---------------
    - For JSON requests: Validates that request.data is accessible after CamelToSnakeMiddleware
    - For multipart POST requests: Validates that request.POST is accessible
    - For multipart PUT/PATCH requests: Manually parses using Django's MultiPartParser
      to validate parsing before other middleware use it
    - Rejects requests if data access or parsing fails, indicating malformed or corrupted requests

    This middleware runs after CamelToSnakeMiddleware to ensure data has been parsed
    and is available for validation.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Union[HttpRequest, Request]) -> Union[HttpResponse, JsonResponse]:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type or ''

            if content_type == 'application/json':
                # For JSON requests, CamelToSnakeMiddleware should have set request.data
                # If accessing it fails, the request is malformed
                if isinstance(request, Request):
                    try:
                        _ = request.data  # type: ignore
                    except Exception as e:
                        logger.warning(f"[ContentValidityMiddleware] Failed to access request.data: {e}")
                        return self._handle_parse_error(ParseError(
                            'Failed to parse request data. The request may be malformed or corrupted.'))

            elif content_type.startswith('multipart/form-data'):
                # For POST requests, validate that request.POST is accessible
                if request.method == 'POST':
                    try:
                        if isinstance(request, Request) and hasattr(request, '_request'):
                            _ = request._request.POST
                        elif hasattr(request, 'POST'):
                            _ = request.POST
                    except Exception as e:
                        logger.warning(f"[ContentValidityMiddleware] Failed to access request.POST: {e}")
                        return self._handle_parse_error(ParseError(
                            'Failed to parse multipart form data. The request may be malformed or corrupted.'))

                # For PUT/PATCH requests, manually parse multipart data using Django's MultiPartParser
                # to validate parsing before other middleware (like ListValueValidationMiddleware) use it
                elif request.method in ['PUT', 'PATCH']:
                    try:
                        from django.core.files.uploadhandler import TemporaryFileUploadHandler
                        from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser
                        from io import BytesIO

                        if not hasattr(request, '_body') or request._body is None:
                            request._body = request.body

                        body_stream = BytesIO(request._body if hasattr(request, '_body')
                                              and request._body else request.body)
                        parser = DjangoMultiPartParser(request.META, body_stream, [TemporaryFileUploadHandler()])
                        parser.parse()

                        # Restore the body stream so DRF can parse it later
                        if hasattr(request, '_body') and request._body:
                            request._stream = BytesIO(request._body)  # type: ignore
                            request._read_started = False  # type: ignore
                    except Exception as e:
                        logger.warning(f"[ContentValidityMiddleware] Failed to parse multipart data: {e}")
                        return self._handle_parse_error(ParseError(
                            'Failed to parse multipart form data. The request may be malformed or corrupted.'))

        response = self.get_response(request)
        return response

    def _handle_parse_error(self, exc: ParseError) -> JsonResponse:
        """Handle parse errors by converting them to proper error responses."""
        return ErrorResponse.handle_exception(exc)
