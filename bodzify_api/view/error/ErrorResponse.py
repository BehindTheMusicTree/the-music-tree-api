from typing import Any, List, Union, Dict

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DrfValidationError, ErrorDetail as DRFErrorDetail
from django.http import JsonResponse
from rest_framework import status

from bodzify_api.view.error.ApiErrorCode import ApiErrorCode
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.view.error.ErrorResponseDetail import ErrorResponseDetail
from bodzify_api.view.error.ErrorHttpStatusCodeMap import ErrorHTTPStatusCodeMap
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.validator.ValidationErrorFields import ValidationErrorFields
from bodzify_api.view.error.ErrorMessages import ErrorMessages


class ErrorResponse:

    @staticmethod
    def _get_error_code(error: Any, default_code: str = 'error') -> str:
        if isinstance(error, dict) and 'unknown_fields' in error:
            return str(error['unknown_fields']['code'])
        if isinstance(error, DRFErrorDetail) and hasattr(error, 'code') and error.code:
            return str(error.code)
        return default_code

    @staticmethod
    def _format_validation_message(message: str, field: str) -> str:
        if message.startswith("{'message': '") and message.endswith("'}"):
            try:
                import json
                parsed = json.loads(message.replace("'", '"'))
                message = parsed.get('message', message)
            except:
                pass
        return message

    @staticmethod
    def _convert_fields_to_list(fields: List[Any]) -> List[str]:
        return [str(field) for field in fields]

    @staticmethod
    def _create_error_response(
            error_detail: Dict[str, Any],
            error_code: ApiErrorCode = ApiErrorCode.VALIDATION_INVALID_INPUT
    ) -> JsonResponse:
        http_status = ErrorHTTPStatusCodeMap.ERROR_TO_HTTP_STATUS.get(error_code, status.HTTP_400_BAD_REQUEST)
        status_message = ErrorHTTPStatusCodeMap.STATUS_MESSAGES.get(http_status, "Bad Request")

        response_data = {
            ErrorResponseFields.CODE: error_code.value,
            ErrorResponseFields.MESSAGE: status_message,
            ErrorResponseFields.SUCCESS: False,
            ErrorResponseFields.DETAILS: [error_detail]
        }

        return JsonResponse(
            data=response_data,
            status=http_status,
            safe=False
        )

    @staticmethod
    def _parse_error_message(error: Any) -> tuple[str, str]:
        """Parse error message and code from various error formats."""
        if isinstance(error, str):
            # Try to parse if it looks like a serialized list/dict
            if error.startswith('[') or error.startswith('{'):
                try:
                    import json
                    parsed = json.loads(error.replace("'", '"'))
                    if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                        return parsed[0]['message'], parsed[0]['code']
                    elif isinstance(parsed, dict):
                        return parsed['message'], parsed['code']
                except:
                    pass
            return error, 'blank' if 'may not be blank' in error else 'invalid'
        if isinstance(error, dict):
            if 'message' in error and 'code' in error:
                return error[ErrorResponseFields.MESSAGE], error[ErrorResponseFields.CODE]
            return str(
                error.get(ErrorResponseFields.MESSAGE, error)), error.get(
                ErrorResponseFields.CODE, ValidationErrorFields.VALIDATION_ERROR)
        return str(error), ValidationErrorFields.VALIDATION_ERROR

    @staticmethod
    def _format_validation_error(error_detail: Dict[str, Any]) -> Dict[str, Any]:
        formatted_errors = {}
        for field, errors in error_detail.items():
            if not isinstance(errors, (list, tuple)):
                errors = [errors]

            field_errors = []
            for error in errors:
                message, code = ErrorResponse._parse_error_message(error)
                field_errors.append({
                    ErrorResponseFields.MESSAGE: message,
                    ErrorResponseFields.CODE: code
                })

            formatted_errors[field] = field_errors

        return {
            ErrorResponseFields.MESSAGE: ErrorMessages.VALIDATION_FAILED,
            ValidationErrorFields.FIELD_ERRORS: formatted_errors
        }

    @staticmethod
    def from_unhandled_integrity_error(exception: IntegrityError) -> JsonResponse:
        error_detail = {
            ErrorResponseFields.MESSAGE: ErrorMessages.INTERNAL_ERROR,
            ErrorResponseFields.CODE: ApiErrorCode.SYSTEM_INTERNAL_ERROR.name.lower()
        }
        return ErrorResponse._create_error_response(
            error_detail=error_detail,
            error_code=ApiErrorCode.SYSTEM_INTERNAL_ERROR
        )

    @staticmethod
    def from_validation_error(
            exception: Union[AppValidationError, DrfValidationError, DjangoValidationError]) -> JsonResponse:
        """Handle various types of validation errors with appropriate formatting."""

        if isinstance(exception, AppValidationError):
            error_detail = exception.get_error_detail()
            formatted_error = {
                ErrorResponseFields.MESSAGE: ErrorMessages.VALIDATION_FAILED,
                ValidationErrorFields.FIELD_ERRORS: {
                    exception.field: [{
                        ErrorResponseFields.MESSAGE: error_detail[ErrorResponseFields.MESSAGE],
                        ErrorResponseFields.CODE: error_detail[ErrorResponseFields.CODE]
                    }]
                }
            }
            return ErrorResponse._create_error_response(
                formatted_error,
                ApiErrorCode.VALIDATION_INVALID_INPUT
            )
        elif isinstance(exception, DrfValidationError):
            error_detail = ErrorResponseDetail.convert_error_detail_to_dict(exception.detail)

            # If it's already a dict with a message, use it directly
            if isinstance(error_detail, dict) and ErrorResponseFields.MESSAGE in error_detail:
                return ErrorResponse._create_error_response(
                    error_detail,
                    ApiErrorCode.VALIDATION_INVALID_INPUT
                )

            # If it's a dict with field errors
            if isinstance(error_detail, dict):
                formatted_error = ErrorResponse._format_validation_error(error_detail)
                return ErrorResponse._create_error_response(
                    formatted_error,
                    ApiErrorCode.VALIDATION_INVALID_INPUT
                )

            # For any other case, wrap it in a standard format
            return ErrorResponse._create_error_response(
                {ErrorResponseFields.MESSAGE: ErrorMessages.VALIDATION_FAILED,
                 ValidationErrorFields.FIELD_ERRORS: error_detail
                 if isinstance(error_detail, dict) else {ErrorResponseFields.DETAIL: error_detail}},
                ApiErrorCode.VALIDATION_INVALID_INPUT)

        if isinstance(exception, DjangoValidationError):
            if hasattr(exception, 'message_dict'):
                # Multiple field errors
                formatted_error = {
                    ErrorResponseFields.MESSAGE: ErrorMessages.VALIDATION_FAILED,
                    ValidationErrorFields.FIELD_ERRORS: {
                        field: [{
                            ErrorResponseFields.MESSAGE: msgs[0],
                            ErrorResponseFields.CODE: ValidationErrorFields.VALIDATION_ERROR
                        }] for field, msgs in exception.message_dict.items()
                    }
                }
                return ErrorResponse._create_error_response(
                    formatted_error,
                    ApiErrorCode.VALIDATION_INVALID_INPUT
                )
            else:
                # Single error message
                formatted_error = {
                    ErrorResponseFields.MESSAGE: ErrorMessages.VALIDATION_FAILED,
                    ValidationErrorFields.FIELD_ERRORS: {
                        ErrorResponseFields.DETAIL: [{
                            ErrorResponseFields.MESSAGE: str(exception.messages[0] if exception.messages else exception),
                            ErrorResponseFields.CODE: ApiErrorCode.VALIDATION_INVALID_INPUT.name.lower()
                        }]
                    }
                }
                return ErrorResponse._create_error_response(
                    formatted_error,
                    ApiErrorCode.VALIDATION_INVALID_INPUT
                )

        # Generic validation error
        error_detail = {
            ErrorResponseFields.MESSAGE: str(exception),
            ErrorResponseFields.CODE: ApiErrorCode.VALIDATION_INVALID_INPUT.name.lower()
        }
        return ErrorResponse._create_error_response(
            error_detail,
            ApiErrorCode.VALIDATION_INVALID_INPUT
        )
