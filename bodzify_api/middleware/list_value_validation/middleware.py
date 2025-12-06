import logging
from typing import Union

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser
from rest_framework.request import Request

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponse import ErrorResponse

logger = logging.getLogger(__name__)


class ListValueValidationMiddleware:
    """
    Middleware to detect and reject list fields containing both empty and non-empty values.

    This middleware enforces a validation rule that list fields (with [] suffix) cannot
    contain both empty values ('', None) and non-empty values in the same list. This prevents
    ambiguous data where it's unclear whether empty values are intentional or accidental.

    Examples:
    - ✅ `artists_names[]=Muse&artists_names[]=Radiohead` (all non-empty)
    - ✅ `artists_names[]=` (all empty - normalized to [] by TestClientEmptyListMiddleware)
    - ❌ `artists_names[]=Muse&artists_names[]=` (mixed empty and non-empty)

    Implementation:
    ---------------
    - For POST requests: Uses request.POST (populated by Django)
    - For PUT/PATCH requests: Manually parses multipart data from raw body since
      Django doesn't populate request.POST for these methods
    - For JSON requests: Checks request.data after DRF parsing
    - Detects violations before serializer normalization to catch them early
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Union[HttpRequest, Request]) -> Union[HttpResponse, JsonResponse]:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type or ''

            if content_type == 'application/json':
                # For JSON, check request.data if available (DRF Request)
                # Note: ContentValidityMiddleware (which runs before this) validates that request.data
                # is accessible, so it should always be available here. If it's not, ContentValidityMiddleware
                # would have already rejected the request.
                if isinstance(request, Request):
                    data = request.data  # type: ignore
                    if isinstance(data, dict):
                        try:
                            self._validate_list_values_json(data)
                        except AppValidationException as e:
                            return self._handle_validation_error(e)

            elif content_type.startswith('multipart/form-data'):
                data_to_check = None

                # For POST requests, Django populates request.POST
                if request.method == 'POST':
                    if isinstance(request, Request) and hasattr(request, '_request'):
                        post_data = request._request.POST
                        if hasattr(post_data, 'getlist') and len(post_data) > 0:
                            data_to_check = post_data
                    elif hasattr(request, 'POST') and len(request.POST) > 0:
                        data_to_check = request.POST

                # For PUT/PATCH requests, manually parse multipart data
                if data_to_check is None and request.method in ['PUT', 'PATCH']:
                    try:
                        if not hasattr(request, '_body') or request._body is None:
                            request._body = request.body

                        # Create a BytesIO stream from the body for parsing
                        from io import BytesIO
                        body_stream = BytesIO(request._body if hasattr(request, '_body')
                                              and request._body else request.body)
                        parser = DjangoMultiPartParser(request.META, body_stream, [TemporaryFileUploadHandler()])
                        parsed_data, files = parser.parse()
                        if isinstance(parsed_data, QueryDict) and len(parsed_data) > 0:
                            data_to_check = parsed_data

                            # Restore the body stream so DRF can parse it later
                            from io import BytesIO
                            if hasattr(request, '_body') and request._body:
                                request._stream = BytesIO(request._body)  # type: ignore
                                request._read_started = False  # type: ignore
                    except Exception as e:
                        # If we can't parse multipart data, this is a parsing failure that should be rejected.
                        # ContentValidityMiddleware (which runs before this) also uses Django's MultiPartParser
                        # to validate parsing, so this should rarely happen. We catch it here as well for
                        # defense in depth.
                        logger.warning(f"[ListValueValidationMiddleware] Failed to parse multipart data: {e}")
                        from rest_framework.exceptions import ParseError
                        return self._handle_parse_error(ParseError(
                            'Failed to parse multipart form data. The request may be malformed or corrupted.'))

                # Validate list values in multipart data
                if data_to_check:
                    try:
                        self._validate_list_values_multipart(data_to_check)
                    except AppValidationException as e:
                        return self._handle_validation_error(e)

        response = self.get_response(request)
        return response

    def _handle_validation_error(self, exc: AppValidationException) -> JsonResponse:
        """Handle validation errors by converting them to proper error responses."""
        return ErrorResponse._from_validation_error(exc)

    def _handle_parse_error(self, exc) -> JsonResponse:
        """Handle parse errors by converting them to proper error responses."""
        from rest_framework.exceptions import ParseError
        return ErrorResponse.handle_exception(exc)

    def _validate_list_values_multipart(self, data: QueryDict | dict) -> None:
        """Validate that list fields don't contain both empty and non-empty values."""
        # Handle both QueryDict (from Django) and dict (from CamelToSnakeMiddleware)
        if isinstance(data, QueryDict):
            items = data.lists()
        else:
            items = data.items()

        for key, value in items:
            # Only check list fields (with [] suffix)
            if key.endswith('[]'):
                # Normalize value to list
                if isinstance(value, list):
                    values = value
                else:
                    values = [value]

                # Only validate if there are multiple values
                if len(values) > 1:
                    has_empty = '' in values or None in values
                    has_non_empty = any(v and v != '' for v in values)

                    if has_empty and has_non_empty:
                        # Convert field name to camelCase for error response
                        from bodzify_api.utils import data_transformer
                        field_name = data_transformer.to_camel_case(key)
                        raise AppValidationException(
                            field_name=field_name,
                            message='Empty values are not allowed when other values are specified',
                            field_validation_error_code=FieldValidationErrorCode.LIST_VALUE_EMPTY
                        )

    def _validate_list_values_json(self, data: dict) -> None:
        """Validate that list fields don't contain both empty and non-empty values in JSON."""
        for key, value in data.items():
            # Check if it's a list field (ends with [] or is a list)
            if isinstance(value, list) and len(value) > 1:
                has_empty = '' in value or None in value
                has_non_empty = any(v and v != '' for v in value)

                if has_empty and has_non_empty:
                    # Convert field name to camelCase for error response
                    from bodzify_api.utils import data_transformer
                    field_name = data_transformer.to_camel_case(key)
                    raise AppValidationException(
                        field_name=field_name,
                        message='Empty values are not allowed when other values are specified',
                        field_validation_error_code=FieldValidationErrorCode.LIST_VALUE_EMPTY
                    )
