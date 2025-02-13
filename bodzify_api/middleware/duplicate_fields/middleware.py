from django.http import HttpRequest, HttpResponse
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from .utils import find_duplicate_fields


class DuplicateFieldsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def _handle_duplicate_field_error_for_content_type_json(self, field_name: str) -> HttpResponse:
        validation_error = AppValidationError.from_middleware(
            field=field_name,
            message='Duplicate field detected.',
            code=FieldValidationErrorCode.FIELD_DUPLICATE
        )
        return ErrorResponse.from_app_validation_error(validation_error)

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
