from typing import Dict, Union, Any, List

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DRFValidationError, ErrorDetail as DRFErrorDetail
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.view.error.ErrorCode import ErrorCode
from bodzify_api.view.error.ErrorDetail import ErrorDetail
from bodzify_api.view.error.ErrorMessages import AppErrorMessages
from bodzify_api.view.error.HTTPStatusCodeMap import HTTPStatusCodeMap


class ErrorResponse:

    @staticmethod
    def create_error_response(
        error_data: Union[Dict[str, Any], str, List[str]],
        error_code: ErrorCode = ErrorCode.VALIDATION_INVALID_INPUT
    ) -> Response:
        """
        Create a standardized error response.

        Args:
            error_data: Error data in various formats
            error_code: Specific error code from ErrorCode enum
        """
        http_status = HTTPStatusCodeMap.ERROR_TO_HTTP_STATUS.get(
            error_code, status.HTTP_400_BAD_REQUEST
        )
        status_message = HTTPStatusCodeMap.STATUS_MESSAGES.get(
            http_status, "Bad Request"
        )

        # Format error_data into a consistent structure
        if isinstance(error_data, str):
            details = ErrorDetail(
                message=error_data,
                code=error_code.name.lower()
            )
        elif isinstance(error_data, list):
            if all(isinstance(item, str) for item in error_data):
                details = [ErrorDetail(
                    message=msg,
                    code=error_code.name.lower()
                ) for msg in error_data]
            else:
                # Already formatted error details
                details = error_data
        elif isinstance(error_data, dict):
            if 'message' in error_data:
                # Single error with additional context
                details = ErrorDetail(**error_data)
            else:
                # Field-level errors
                details = {}
                for field, errors in error_data.items():
                    if isinstance(errors, (list, tuple)):
                        details[field] = [
                            ErrorDetail(message=str(error), code=error_code.name.lower())
                            for error in errors
                        ]
                    else:
                        details[field] = ErrorDetail(
                            message=str(errors),
                            code=error_code.name.lower()
                        )
        else:
            details = ErrorDetail(
                message=str(error_data),
                code=error_code.name.lower()
            )

        # Convert ErrorDetail instances to dictionaries for JSON serialization
        if isinstance(details, ErrorDetail):
            details = {
                'message': details.message,
                'code': details.code,
                **(({'details': details.details} if details.details else {}))
            }
        elif isinstance(details, list):
            details = [
                {
                    'message': d.message,
                    'code': d.code,
                    **(({'details': d.details} if d.details else {}))
                }
                if isinstance(d, ErrorDetail) else d
                for d in details
            ]
        elif isinstance(details, dict):
            details = {
                k: ({
                    'message': v.message,
                    'code': v.code,
                    **(({'details': v.details} if v.details else {}))
                } if isinstance(v, ErrorDetail) else v)
                for k, v in details.items()
            }

        return Response(
            data={
                'code': error_code.value,
                'status': str(http_status),
                'message': status_message,
                'success': False,
                'details': details
            },
            status=http_status
        )

    @staticmethod
    def from_validation_error(exc: Union[DRFValidationError, DjangoValidationError, IntegrityError]) -> Response:
        if isinstance(exc, IntegrityError):
            return ErrorResponse.create_error_response(
                {'message': AppErrorMessages.MESSAGES[ErrorCode.VALIDATION_INTEGRITY_ERROR]},
                ErrorCode.VALIDATION_INTEGRITY_ERROR
            )

        if isinstance(exc, DRFValidationError):
            if isinstance(exc.detail, dict):
                error_dict = {}
                for field, errors in exc.detail.items():
                    if isinstance(errors, (list, tuple)):
                        error_dict[field] = [
                            ErrorDetail(
                                message=str(error),
                                code=error.code if isinstance(error, DRFErrorDetail) else 'error'
                            ) for error in errors
                        ]
                    else:
                        error_dict[field] = ErrorDetail(
                            message=str(errors),
                            code=errors.code if isinstance(errors, DRFErrorDetail) else 'error'
                        )
                return ErrorResponse.create_error_response(error_dict, ErrorCode.VALIDATION_INVALID_INPUT)

            if isinstance(exc.detail, (list, tuple)):
                error_details = []
                for error in exc.detail:
                    if isinstance(error, DRFErrorDetail):
                        detail = ErrorDetail(
                            message=str(error),
                            code=error.code
                        )
                        if error.code == 'invalid':
                            detail.details = AppErrorMessages.MESSAGES[ErrorCode.VALIDATION_INVALID_INPUT]
                        error_details.append(detail)
                    else:
                        error_details.append(ErrorDetail(
                            message=str(error),
                            code='error'
                        ))
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
            return ErrorResponse.create_error_response(
                [{'message': msg} for msg in exc.messages],
                ErrorCode.VALIDATION_INVALID_INPUT
            )

        return ErrorResponse.create_error_response({'message': str(exc)})
