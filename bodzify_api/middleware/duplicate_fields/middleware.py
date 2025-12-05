import json
import logging
from typing import Any, Union

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser
from rest_framework.request import Request

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from .JsonDuplicateKeyDetectingDecoder import JsonDuplicateKeyDetectingDecoder

logger = logging.getLogger(__name__)


class DuplicateFieldsMiddleware:
    """
    Middleware to detect and reject duplicate fields in multipart/form-data requests.

    Note on Multipart Form Data Standards:
    --------------------------------------
    According to the HTTP specification (RFC 7578), duplicate field names are
    standard and allowed in multipart/form-data. Many web forms legitimately use
    the same field name for multiple values (e.g., checkboxes, multiple file uploads).

    However, this application enforces a validation rule that rejects duplicate fields
    to prevent confusion and ensure data integrity. This is an application-level
    constraint, not a protocol requirement.

    Exception:
    ----------
    List fields with a '[]' suffix (e.g., 'artists_names[]') are allowed to have
    multiple values, as this is the intended way to send arrays in multipart form data.

    Implementation:
    ---------------
    - For POST requests: Uses request.POST (populated by Django)
    - For PUT/PATCH requests: Manually parses multipart data from raw body since
      Django doesn't populate request.POST for these methods
    - Detects duplicates before DRF normalization to catch them early
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def find_duplicate_fields_in_json(self, json_str: str) -> list[str]:
        try:
            decoder = JsonDuplicateKeyDetectingDecoder()
            decoder.decode(json_str)
            return decoder.tracker.duplicates
        except json.JSONDecodeError:
            return []

    def handle_duplicate_field(self, field_name: str) -> JsonResponse:
        """Handle duplicate field by creating an AppValidationException and converting it to response."""
        exception = AppValidationException(
            field_name=field_name,
            message='Duplicate field detected.',
            field_validation_error_code=FieldValidationErrorCode.DUPLICATE
        )
        return ErrorResponse._from_validation_error(exception)

    def __call__(self, request: Union[HttpRequest, Request]) -> Union[HttpResponse, JsonResponse]:
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type or ''

            if content_type == 'application/json':
                try:
                    raw_body = request.body.decode('utf-8')
                    duplicate_fields = self.find_duplicate_fields_in_json(raw_body)
                    if duplicate_fields:
                        # Handle the duplicate field directly instead of raising
                        return self.handle_duplicate_field(duplicate_fields[0])
                except UnicodeDecodeError:
                    # Let system errors propagate up to be handled by global error handler
                    raise
            elif content_type.startswith('multipart/form-data'):
                # For multipart requests, check raw POST data (QueryDict) before DRF parsing
                # This allows us to detect duplicate fields before normalization
                data_to_check = None

                # For POST requests, Django populates request.POST, so we can use it directly
                # For PUT/PATCH requests, Django doesn't populate request.POST, so we must use request.data
                if request.method == 'POST':
                    if isinstance(request, Request) and hasattr(request, '_request'):
                        post_data = request._request.POST
                        # QueryDict has getlist() method (lowercase)
                        if hasattr(post_data, 'getlist') and len(post_data) > 0:
                            data_to_check = post_data
                    elif hasattr(request, 'POST') and len(request.POST) > 0:
                        data_to_check = request.POST

                # For PUT/PATCH requests, we must parse multipart data manually since request.POST is empty
                # and request.data is not available in middleware (only available in DRF views)
                if data_to_check is None and request.method in ['PUT', 'PATCH']:
                    try:
                        # Manually parse multipart data from raw body to detect duplicates
                        # This is necessary because Django doesn't populate request.POST for PUT/PATCH
                        parser = DjangoMultiPartParser(request.META, request, [TemporaryFileUploadHandler()])
                        parsed_data, _ = parser.parse()
                        if isinstance(parsed_data, QueryDict) and len(parsed_data) > 0:
                            data_to_check = parsed_data
                    except Exception as e:
                        logger.info(f"[DuplicateFieldsMiddleware] Failed to manually parse multipart data: {e}")
                        # Fall through to check request.data if it's a Request instance

                # If still no data, try request.data (for DRF Request instances)
                # Note: accessing request.data triggers parsing, but we check it before normalization
                # DRF's MultiPartParser returns QueryDict for multipart requests (both POST and PUT)
                if data_to_check is None:
                    if isinstance(request, Request):
                        # Access request.data to trigger DRF parsing
                        # DRF's MultiPartParser returns QueryDict for multipart requests
                        data_to_check = request.data  # type: Any
                    # Fallback to request.POST only if request.data is not available
                    elif hasattr(request, 'POST') and len(request.POST) > 0:
                        data_to_check = request.POST
                    elif hasattr(request, 'POST'):
                        data_to_check = request.POST

                # Only check if we have data to check
                if data_to_check:
                    seen_fields = {}
                    duplicates = []

                    # Check for duplicates while allowing list fields
                    for field_name in data_to_check.keys():
                        # Skip list fields (fields with [] suffix are allowed to have multiple values)
                        if field_name.endswith('[]'):
                            continue

                        # Check if field has multiple values (from multipart form data)
                        # QueryDict (from both POST and PUT) has getlist() method (lowercase)
                        if hasattr(data_to_check, 'getlist'):  # Handle QueryDict (POST and PUT)
                            values = data_to_check.getlist(field_name)
                            has_multiple_values = len(values) > 1
                        else:  # Handle regular dict (fallback, though MultiPartParser should return QueryDict)
                            value = data_to_check.get(field_name)
                            # Multiple values in multipart form data appear as lists in request.data
                            # DRF's MultiPartParser converts duplicate fields to lists
                            has_multiple_values = isinstance(value, (list, tuple)) and len(value) > 1

                        # Multiple values for non-list field indicates duplicate fields in form
                        if has_multiple_values:
                            duplicates.append(field_name)
                            continue

                        if field_name in seen_fields:
                            duplicates.append(field_name)
                        else:
                            seen_fields[field_name] = True

                    if duplicates:
                        # Handle the duplicate field directly instead of raising
                        return self.handle_duplicate_field(duplicates[0])

        return self.get_response(request)
