from typing import Dict, Union, Any, Sequence, cast, List

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DrfValidationError, ErrorDetail as DRFErrorDetail
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.view.error.ErrorCode import ErrorCode
from bodzify_api.view.error.ErrorDetail import ErrorDetail
from bodzify_api.view.error.ErrorMessages import AppErrorMessages
from bodzify_api.view.error.ErrorHttpStatusCodeMap import ErrorHTTPStatusCodeMap

# Type for error data that can be passed to create_error_response
ErrorDataType = Union[Dict[str, Any], str, Sequence[Union[str, Dict[str, Any]]]]


def convert_error_detail(obj: Any) -> Any:
    """Recursively convert ErrorDetail instances to dictionaries."""
    if isinstance(obj, ErrorDetail):
        return obj.to_dict()
    elif isinstance(obj, list):
        return [convert_error_detail(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_error_detail(value) for key, value in obj.items()}
    return obj


class ErrorResponse:

    @staticmethod
    def _get_error_code(error: Any, default_code: str = 'error') -> str:
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
    def create_error_response(error_data: ErrorDataType, error_code: ErrorCode = ErrorCode.VALIDATION_INVALID_INPUT
                              ) -> Response:
        http_status = ErrorHTTPStatusCodeMap.ERROR_TO_HTTP_STATUS.get(error_code, status.HTTP_400_BAD_REQUEST)
        status_message = ErrorHTTPStatusCodeMap.STATUS_MESSAGES.get(http_status, "Bad Request")

        # Format error_data into a consistent structure
        if isinstance(error_data, str):
            details = [{'message': error_data, 'code': error_code.name.lower()}]
        elif isinstance(error_data, (list, tuple)):
            if all(isinstance(item, str) for item in error_data):
                details = [{'message': str(msg), 'code': error_code.name.lower()} for msg in error_data]
            else:
                details = [{'message': str(error.message if isinstance(error, ErrorDetail) else error),
                            'code': error_code.name.lower()} for error in error_data]
        elif isinstance(error_data, dict):
            if 'message' in error_data:
                error_dict = error_data.copy()
                if 'code' not in error_dict:
                    error_dict['code'] = error_code.name.lower()

                # Extract field name if present
                field = next((k for k in error_dict.keys() if k not in {'message', 'code', 'details'}), None)
                message = str(error_dict['message'])
                if field:
                    message = ErrorResponse._format_validation_message(message, field)

                details = [{
                    'message': message,
                    'code': str(error_dict['code']),
                    'field': field
                }]
            else:
                details = []
                for field, errors in error_data.items():
                    if isinstance(errors, (list, tuple)):
                        for error in errors:
                            error_msg = str(error.message if isinstance(error, ErrorDetail) else error)
                            error_msg = ErrorResponse._format_validation_message(error_msg, field)
                            error_code_value = ErrorResponse._get_error_code(error) if isinstance(
                                error, DRFErrorDetail) else error_code.name.lower()
                            details.append({
                                'message': error_msg,
                                'code': error_code_value,
                                'field': field
                            })
                    else:
                        error_msg = str(errors)
                        error_msg = ErrorResponse._format_validation_message(error_msg, field)
                        error_code_value = ErrorResponse._get_error_code(errors) if isinstance(
                            errors, DRFErrorDetail) else error_code.name.lower()
                        details.append({
                            'message': error_msg,
                            'code': error_code_value,
                            'field': field
                        })
        else:
            details = [{'message': str(error_data), 'code': error_code.name.lower()}]

        # Create response data dictionary
        response_data = {
            'code': error_code.value,
            'message': status_message,
            'success': False,
            'details': details
        }

        return Response(
            data=response_data,
            status=http_status,
            content_type='application/json'
        )

    @staticmethod
    def from_validation_error(exc: Union[DrfValidationError, DjangoValidationError, IntegrityError]) -> Response:
        if isinstance(exc, IntegrityError):
            return ErrorResponse.create_error_response(
                {'message': AppErrorMessages.MESSAGES[ErrorCode.VALIDATION_INTEGRITY_ERROR]},
                ErrorCode.VALIDATION_INTEGRITY_ERROR
            )

        if isinstance(exc, DrfValidationError):
            if isinstance(exc.detail, dict):
                error_dict = {}
                for field, errors in exc.detail.items():
                    if isinstance(errors, (list, tuple)):
                        error_dict[field] = [
                            {'message': str(error), 'code': ErrorResponse._get_error_code(error), 'field': field}
                            for error in errors
                        ]
                    else:
                        error_dict[field] = {
                            'message': str(errors),
                            'code': ErrorResponse._get_error_code(errors),
                            'field': field
                        }
                return ErrorResponse.create_error_response(error_dict, ErrorCode.VALIDATION_INVALID_INPUT)

            if isinstance(exc.detail, (list, tuple)):
                error_details = [
                    {'message': str(error), 'code': ErrorResponse._get_error_code(error)}
                    for error in exc.detail
                ]
                return ErrorResponse.create_error_response(error_details, ErrorCode.VALIDATION_INVALID_INPUT)

            return ErrorResponse.create_error_response(
                {'message': str(exc.detail)},
                ErrorCode.VALIDATION_INVALID_INPUT
            )

        if isinstance(exc, DjangoValidationError):
            if hasattr(exc, 'message_dict'):
                error_dict = {}
                for field, messages in exc.message_dict.items():
                    error_dict[field] = [
                        {'message': str(msg), 'code': ErrorCode.VALIDATION_INVALID_INPUT.name.lower(), 'field': field}
                        for msg in messages
                    ]
                return ErrorResponse.create_error_response(error_dict, ErrorCode.VALIDATION_INVALID_INPUT)

            error_list = [
                {'message': str(msg), 'code': ErrorCode.VALIDATION_INVALID_INPUT.name.lower()}
                for msg in exc.messages
            ]
            return ErrorResponse.create_error_response(error_list, ErrorCode.VALIDATION_INVALID_INPUT)

        return ErrorResponse.create_error_response({'message': str(exc)})
