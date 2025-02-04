from typing import Any, List, Union, Dict

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DrfValidationError, ErrorDetail as DRFErrorDetail
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.view.error.ApiErrorCode import ApiErrorCode
from bodzify_api.view.error.ErrorResponseDetail import ErrorResponseDetail
from bodzify_api.view.error.ErrorHttpStatusCodeMap import ErrorHTTPStatusCodeMap


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
    ) -> Response:
        http_status = ErrorHTTPStatusCodeMap.ERROR_TO_HTTP_STATUS.get(error_code, status.HTTP_400_BAD_REQUEST)
        status_message = ErrorHTTPStatusCodeMap.STATUS_MESSAGES.get(http_status, "Bad Request")

        response_data = {
            'code': error_code.value,
            'message': status_message,
            'success': False,
            'details': [error_detail]
        }

        return Response(
            data=response_data,
            status=http_status,
            content_type='application/json'
        )

    @staticmethod
    def from_unhandled_integrity_error(exception: IntegrityError) -> Response:
        error_detail = {
            'message': 'An internal error occurred',
            'code': ApiErrorCode.SYSTEM_INTERNAL_ERROR.name.lower()
        }
        return ErrorResponse._create_error_response(
            error_detail=error_detail,
            error_code=ApiErrorCode.SYSTEM_INTERNAL_ERROR
        )

    @staticmethod
    def _format_validation_error(error_detail: Dict[str, Any]) -> Dict[str, Any]:
        formatted_errors = {}
        for field, error in error_detail.items():
            if not isinstance(error, dict):
                formatted_errors[field] = error
                continue

            # Extract error details safely
            message = error.get('message', 'Validation error occurred')
            code = error.get('code', 'validation_error')
            formatted_errors[field] = {
                'message': message,
                'code': code
            }

        return {
            'message': 'Validation failed',
            'field_errors': formatted_errors
        }

    @staticmethod
    def from_validation_error(exception: Union[DrfValidationError, DjangoValidationError]) -> Response:
        if isinstance(exception, DrfValidationError):
            error_detail = ErrorResponseDetail.convert_error_detail_to_dict(exception.detail)
            if isinstance(error_detail, dict):
                # Handle field validation errors (already properly structured by DRF)
                if any(isinstance(v, dict) for v in error_detail.values()):
                    formatted_error = ErrorResponse._format_validation_error(error_detail)
                    return ErrorResponse._create_error_response(
                        formatted_error,
                        ApiErrorCode.VALIDATION_INVALID_INPUT
                    )
                # For simple validation errors with message
                if 'message' in error_detail:
                    return ErrorResponse._create_error_response(
                        error_detail,
                        ApiErrorCode.VALIDATION_INVALID_INPUT
                    )

            # Fallback for any other validation error structure
            return ErrorResponse._create_error_response(
                {'message': 'Validation error', 'errors': error_detail},
                ApiErrorCode.VALIDATION_INVALID_INPUT
            )

        if isinstance(exception, DjangoValidationError):
            if hasattr(exception, 'message_dict'):
                # Multiple field errors
                error_detail = {
                    field: {'message': msgs[0], 'code': 'validation_error'}
                    for field, msgs in exception.message_dict.items()
                }
                formatted_error = ErrorResponse._format_validation_error(error_detail)
                return ErrorResponse._create_error_response(
                    formatted_error,
                    ApiErrorCode.VALIDATION_INVALID_INPUT
                )
            else:
                # Single error message
                error_detail = {
                    'message': str(exception.messages[0] if exception.messages else exception),
                    'code': ApiErrorCode.VALIDATION_INVALID_INPUT.name.lower()
                }
                return ErrorResponse._create_error_response(
                    error_detail,
                    ApiErrorCode.VALIDATION_INVALID_INPUT
                )

        # Generic validation error
        error_detail = {
            'message': str(exception),
            'code': ApiErrorCode.VALIDATION_INVALID_INPUT.name.lower()
        }
        return ErrorResponse._create_error_response(
            error_detail,
            ApiErrorCode.VALIDATION_INVALID_INPUT
        )
