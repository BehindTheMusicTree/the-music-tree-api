from typing import Any, Dict, List, Union

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail as DRFErrorDetail
from rest_framework.exceptions import ValidationError as DrfValidationError

from bodzify_api.exception.validation.app.AppValidationError import \
    AppValidationException
from bodzify_api.exception.validation.app.AppValidationErrorFields import \
    AppValidationErrorFields
from bodzify_api.exception.validation.DrfValidationErrorFields import \
    DrfValidationErrorFields
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.view.error.ApiErrorCode import ApiErrorCode
from bodzify_api.view.error.DrfValidationErrorResponseDetail import \
    DrfValidationErrorResponseDetail
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class ErrorResponse:

    @staticmethod
    def _get_error_code(error: Any, default_code: str = 'error') -> str:
        if isinstance(error, Dict) and 'unknown_fields' in error:
            return str(error['unknown_fields'][DrfValidationErrorFields.CODE])
        if isinstance(error, DRFErrorDetail) and hasattr(error, 'code') and error.code:
            return str(error.code)
        return default_code

    @staticmethod
    def _convert_fields_to_list(fields: List[Any]) -> List[str]:
        return [str(field) for field in fields]

    @staticmethod
    def _create_error_response(
            error_detail: Dict[str, Any],
            error_code: ApiErrorCode = ApiErrorCode.VALIDATION_INVALID_INPUT
    ) -> JsonResponse:
        http_status = ErrorResponseFields.ERROR_TO_HTTP_STATUS.get(error_code, status.HTTP_400_BAD_REQUEST)
        status_message = ErrorResponseFields.STATUS_MESSAGES.get(http_status, "An error occurred")

        response_data = {
            ErrorResponseFields.FieldErrors.CODE: error_code.value,
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
            # Try to parse if it looks like a serialized list/Dict
            if error.startswith('[') or error.startswith('{'):
                try:
                    import json
                    parsed = json.loads(error.replace("'", '"'))
                    if isinstance(parsed, list) and parsed and isinstance(parsed[0], Dict):
                        return parsed[0]['message'], parsed[0]['code']
                    elif isinstance(parsed, Dict):
                        return parsed['message'], parsed['code']
                except:
                    pass
            return error, 'blank' if 'may not be blank' in error else 'invalid'
        if isinstance(error, Dict):
            if DrfValidationErrorFields.MESSAGE in error and DrfValidationErrorFields.CODE in error:
                return error[ErrorResponseFields.MESSAGE], error[ErrorResponseFields.CODE]
            return str(error.get(DrfValidationErrorFields.MESSAGE, error)), \
                error.get(DrfValidationErrorFields.CODE,
                          ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE)
        return str(error), ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE

    @staticmethod
    def _format_from_drf_validation_error_detail(error_detail: Dict[str, Any]) -> Dict[str, Any]:
        formatted_errors = {}
        for field, errors in error_detail.items():
            if not isinstance(errors, (list, tuple)):
                errors = [errors]

            camel_case_field = to_camel_case(field)
            field_errors = []
            for error in errors:
                message, code = ErrorResponse._parse_error_message(error)
                field_errors.append({
                    ErrorResponseFields.MESSAGE: message,
                    ErrorResponseFields.CODE: code
                })

            formatted_errors[camel_case_field] = field_errors

        return {
            ErrorResponseFields.MESSAGE: ErrorResponseFields.MESSAGES[ApiErrorCode.VALIDATION_INVALID_INPUT],
            ErrorResponseFields.FIELD_ERRORS: formatted_errors
        }

    @staticmethod
    def from_unhandled_integrity_error(exception: IntegrityError) -> JsonResponse:
        error_detail = {
            ErrorResponseFields.FieldErrors.MESSAGE:
            ErrorResponseFields.DefaultFieldValidationValues.DbIntegrityError.MESSAGE,
            ErrorResponseFields.FieldErrors.CODE: ApiErrorCode.SYSTEM_INTERNAL_ERROR.value
        }
        return ErrorResponse._create_error_response(
            error_detail=error_detail,
            error_code=ApiErrorCode.SYSTEM_INTERNAL_ERROR
        )

    @staticmethod
    def from_validation_error(
            exception: Union[AppValidationException, DrfValidationError, DjangoValidationError]) -> JsonResponse:

        if isinstance(exception, AppValidationException):

            formatted_error = {
                ErrorResponseFields.MESSAGE: ErrorResponseFields.MESSAGES[ApiErrorCode.VALIDATION_INVALID_INPUT],
                ErrorResponseFields.FIELD_ERRORS: {
                    to_camel_case(field): [{
                        ErrorResponseFields.FieldErrors.MESSAGE: error_detail[AppValidationErrorFields.MESSAGE],
                        ErrorResponseFields.FieldErrors.CODE: error_detail[AppValidationErrorFields.CODE]
                    }]
                    for field, error_detail in exception.errors.items()
                }
            }
            return ErrorResponse._create_error_response(
                error_detail=formatted_error,
                error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
            )
        elif isinstance(exception, DrfValidationError):
            error_detail = DrfValidationErrorResponseDetail.convert_error_detail_to_dict(exception.detail)

            # If it's already a Dict with a message, use it directly
            if isinstance(error_detail, Dict) and ErrorResponseFields.MESSAGE in error_detail:
                return ErrorResponse._create_error_response(
                    error_detail=error_detail,
                    error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
                )

            # If it's a Dict with field errors
            if isinstance(error_detail, Dict):
                formatted_error = ErrorResponse._format_from_drf_validation_error_detail(error_detail)
                return ErrorResponse._create_error_response(
                    error_detail=formatted_error,
                    error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
                )

            # For any other case, wrap it in a standard format
            return ErrorResponse._create_error_response(
                {ErrorResponseFields.MESSAGE: ErrorResponseFields.MESSAGES[ApiErrorCode.VALIDATION_INVALID_INPUT],
                 ErrorResponseFields.FIELD_ERRORS: error_detail
                 if isinstance(error_detail, Dict) else {ErrorResponseFields.DETAILS: error_detail}},
                ApiErrorCode.VALIDATION_INVALID_INPUT)

        if isinstance(exception, DjangoValidationError):
            if hasattr(exception, 'message_dict'):
                # Multiple field errors
                formatted_error = {
                    ErrorResponseFields.MESSAGE: ErrorResponseFields.MESSAGES[ApiErrorCode.VALIDATION_INVALID_INPUT],
                    ErrorResponseFields.FIELD_ERRORS: {
                        to_camel_case(field): [{
                            ErrorResponseFields.FieldErrors.MESSAGE: msgs[0],
                            ErrorResponseFields.FieldErrors.CODE:
                                ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE
                        }] for field, msgs in exception.message_dict.items()
                    }
                }
                return ErrorResponse._create_error_response(
                    error_detail=formatted_error,
                    error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
                )
            else:
                # Single error message
                formatted_error = {
                    ErrorResponseFields.MESSAGE: ErrorResponseFields.MESSAGES[ApiErrorCode.VALIDATION_INVALID_INPUT],
                    ErrorResponseFields.FIELD_ERRORS: {
                        ErrorResponseFields.DETAILS: [{
                            ErrorResponseFields.FieldErrors.MESSAGE:
                                str(exception.messages[0] if exception.messages else exception),
                            ErrorResponseFields.FieldErrors.CODE:
                                ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE
                        }]
                    }
                }
                return ErrorResponse._create_error_response(
                    error_detail=formatted_error,
                    error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
                )

        # Generic validation error
        error_detail = {
            ErrorResponseFields.MESSAGE: str(exception),
            ErrorResponseFields.CODE: ApiErrorCode.VALIDATION_INVALID_INPUT.name.lower()
        }
        return ErrorResponse._create_error_response(
            error_detail=error_detail,
            error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
        )
