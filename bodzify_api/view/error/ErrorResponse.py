from typing import Dict, Union, Any, Sequence, cast

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
    def create_error_response(error_data: ErrorDataType, error_code: ErrorCode = ErrorCode.VALIDATION_INVALID_INPUT
                              ) -> Response:
        http_status = ErrorHTTPStatusCodeMap.ERROR_TO_HTTP_STATUS.get(error_code, status.HTTP_400_BAD_REQUEST)
        status_message = ErrorHTTPStatusCodeMap.STATUS_MESSAGES.get(http_status, "Bad Request")

        # Format error_data into a consistent structure
        if isinstance(error_data, str):
            details = [ErrorDetail(message=error_data, code=error_code.name.lower()).to_dict()]
        elif isinstance(error_data, (list, tuple)):
            if all(isinstance(item, str) for item in error_data):
                details = [ErrorDetail(message=str(msg), code=error_code.name.lower()).to_dict() for msg in error_data]
            else:
                details = [ErrorDetail(
                    message=str(error.message if isinstance(error, ErrorDetail) else error),
                    code=error_code.name.lower()
                ).to_dict() for error in error_data]
        elif isinstance(error_data, dict):
            if 'message' in error_data:
                error_dict = error_data.copy()
                if 'code' not in error_dict:
                    error_dict['code'] = error_code.name.lower()
                details = [ErrorDetail(
                    message=str(error_dict['message']),
                    code=str(error_dict['code']),
                    details=error_dict.get('details')
                ).to_dict()]
            else:
                details = []
                for field, errors in error_data.items():
                    if isinstance(errors, (list, tuple)):
                        details.extend([
                            ErrorDetail(
                                message=str(error.message if isinstance(error, ErrorDetail) else error),
                                code=error_code.name.lower()
                            ).to_dict()
                            for error in errors
                        ])
                    else:
                        details.append(ErrorDetail(message=str(errors), code=error_code.name.lower()).to_dict())
        else:
            details = [ErrorDetail(message=str(error_data), code=error_code.name.lower()).to_dict()]

        # Create response data dictionary
        response_data = {
            'code': error_code.value,
            'status': str(http_status),
            'message': status_message,
            'success': False,
            'details': details
        }

        return Response(
            data=response_data,  # Pass the dictionary directly, let DRF handle the JSON encoding
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
                            ErrorDetail(
                                message=str(error),
                                code=ErrorResponse._get_error_code(error)
                            ) for error in errors
                        ]
                    else:
                        error_dict[field] = ErrorDetail(
                            message=str(errors),
                            code=ErrorResponse._get_error_code(errors)
                        )
                return ErrorResponse.create_error_response(error_dict, ErrorCode.VALIDATION_INVALID_INPUT)

            if isinstance(exc.detail, (list, tuple)):
                error_details = []
                for error in exc.detail:
                    code = ErrorResponse._get_error_code(error)
                    detail = ErrorDetail(
                        message=str(error),
                        code=code
                    )
                    if code == 'invalid':
                        detail.details = AppErrorMessages.MESSAGES[ErrorCode.VALIDATION_INVALID_INPUT]
                    error_details.append(detail)
                return ErrorResponse.create_error_response(error_details, ErrorCode.VALIDATION_INVALID_INPUT)

            return ErrorResponse.create_error_response(
                {'message': str(exc.detail)},
                ErrorCode.VALIDATION_INVALID_INPUT
            )

        if isinstance(exc, DjangoValidationError):
            if hasattr(exc, 'message_dict'):
                return ErrorResponse.create_error_response(
                    exc.message_dict,
                    ErrorCode.VALIDATION_INVALID_INPUT
                )
            error_list = [
                {'message': str(msg), 'code': ErrorCode.VALIDATION_INVALID_INPUT.name.lower()}
                for msg in exc.messages
            ]
            return ErrorResponse.create_error_response(
                cast(ErrorDataType, error_list),
                ErrorCode.VALIDATION_INVALID_INPUT
            )

        return ErrorResponse.create_error_response({'message': str(exc)})
