from typing import Any, Union

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail as DRFErrorDetail
from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import NotAuthenticated, ParseError, UnsupportedMediaType, MethodNotAllowed

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from bodzify_api.view.error.DrfValidationErrorResponseDetail import DrfValidationErrorResponseDetail
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class ErrorResponse:

    @staticmethod
    def _get_error_code(error: Any, default_code: str = 'error') -> str:
        if isinstance(error, dict) and 'unknown_fields' in error:
            return str(error['unknown_fields']['code'])
        if isinstance(error, DRFErrorDetail):
            return str(error.code) if hasattr(error, 'code') else default_code
        return default_code

    @staticmethod
    def _convert_fields_to_list(fields: list[Any]) -> list[str]:
        return [str(field) for field in fields]

    @staticmethod
    def create_error_response(
        error_detail: dict[str, Any], api_error_code: ApiErrorCodeNumeric = ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT
    ) -> JsonResponse:
        http_status = ErrorResponseFields.ERROR_TO_HTTP_STATUS.get(api_error_code, status.HTTP_400_BAD_REQUEST)
        status_message = ErrorResponseFields.STATUS_MESSAGES.get(http_status, "An error occurred")

        response_data = {
            'code': api_error_code,
            'message': status_message,
            ErrorResponseFields.SUCCESS: False,
            ErrorResponseFields.DETAILS: error_detail
        }

        return JsonResponse(data=response_data, status=http_status, safe=False)

    @staticmethod
    def _parse_error_message_from_various_error_formats(error: Any) -> tuple[str, str]:
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
            return error, FieldValidationErrorCode.DEFAULT
        if isinstance(error, dict):
            if 'message' in error and 'code' in error:
                return error['message'], error['code']
            return str(error.get('message', error)), \
                error.get('code', ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE)
        return str(error), ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE

    @staticmethod
    def _format_from_drf_validation_error_detail(error_detail: dict[str, Any]) -> dict[str, Any]:
        formatted_errors = {}
        for field, errors in error_detail.items():
            if not isinstance(errors, (list, tuple)):
                errors = [errors]

            camel_case_field = to_camel_case(field)
            field_errors = []
            for error in errors:
                message, code = ErrorResponse._parse_error_message_from_various_error_formats(error)
                field_errors.append({'message': message, 'code': code})

            formatted_errors[camel_case_field] = field_errors

        return {
            'message': ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT],
            ErrorResponseFields.FIELD_ERRORS: formatted_errors
        }

    @staticmethod
    def _from_invalid_jwt_token(exception: InvalidToken | NotAuthenticated) -> JsonResponse:
        detail = exception.detail
        message = detail['detail'] if isinstance(detail, dict) and 'detail' in detail else exception.default_detail
        code = detail['code'] if isinstance(detail, dict) and 'code' in detail else exception.default_code
        return ErrorResponse.create_error_response(
            error_detail={'message': message, 'code': code},
            api_error_code=ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS)

    @staticmethod
    def _from_unhandled_integrity_error(exception: IntegrityError) -> JsonResponse:
        error_detail: dict[str, Any] = {
            'message': ErrorResponseFields.DefaultFieldValidationValues.DbIntegrityError.MESSAGE,
            'code': ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR
        }
        return ErrorResponse.create_error_response(
            error_detail=error_detail, api_error_code=ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR)

    @staticmethod
    def _from_unsupported_media_type_exception(exception: UnsupportedMediaType) -> JsonResponse:
        detail = exception.detail
        message = detail['detail'] if isinstance(detail, dict) and 'detail' in detail else exception.default_detail
        return ErrorResponse.create_error_response(
            error_detail={
                'message': message,
                'code': 'unsupported_media_type'
            },
            api_error_code=ApiErrorCodeNumeric.VALIDATION_UNSUPPORTED_MEDIA_TYPE)

    @staticmethod
    def _from_content_type_exception(exception: ParseError) -> JsonResponse:
        detail = exception.detail
        message = detail['detail'] if isinstance(detail, dict) and 'detail' in detail else exception.default_detail
        code = detail['code'] if isinstance(detail, dict) and 'code' in detail else exception.default_code
        return ErrorResponse.create_error_response(
            error_detail={'message': message, 'code': code},
            api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT)

    @staticmethod
    def _from_unhandled_exception(exception: Exception) -> JsonResponse:
        error_detail: dict[str, Any] = {
            'message': "An internal error occurred",
            'code': 'internal_error'
        }
        return ErrorResponse.create_error_response(
            error_detail=error_detail, api_error_code=ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR)

    @staticmethod
    def _from_validation_error(
            exception: Union[AppValidationException, DrfValidationError, DjangoValidationError]) -> JsonResponse:

        if isinstance(exception, AppValidationException):

            formatted_error = {
                'message': ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT],
                'code': 'invalid_input',
                ErrorResponseFields.FIELD_ERRORS: {
                    to_camel_case(field): [{
                        'message': error_detail['message'],
                        'code': error_detail['code']
                    }]
                    for field, error_detail in exception.errors.items()
                }
            }
            return ErrorResponse.create_error_response(
                error_detail=formatted_error,
                api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT
            )
        elif isinstance(exception, DrfValidationError):
            error_detail = DrfValidationErrorResponseDetail.convert_error_detail_to_dict(exception.detail)

            # If it's already a dict with a message, use it directly
            if isinstance(error_detail, dict) and 'message' in error_detail:
                return ErrorResponse.create_error_response(
                    error_detail=error_detail, api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT)

            # If it's a dict with field errors
            if isinstance(error_detail, dict):
                formatted_error = ErrorResponse._format_from_drf_validation_error_detail(error_detail)
                return ErrorResponse.create_error_response(
                    error_detail=formatted_error, api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT)

            # For any other case, wrap it in a standard format
            return ErrorResponse.create_error_response(
                {
                    'message': ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT],
                    'code': 'invalid_input',
                    ErrorResponseFields.FIELD_ERRORS: error_detail
                    if isinstance(error_detail, dict) else {ErrorResponseFields.DETAILS: error_detail}
                },
                ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT)

        if isinstance(exception, DjangoValidationError):
            if hasattr(exception, 'message_dict'):
                # Multiple field errors
                formatted_error = {
                    'message': ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT],
                    'code': 'invalid_input',
                    ErrorResponseFields.FIELD_ERRORS: {
                        to_camel_case(field): [{
                            'message': msgs[0],
                            'code': ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE
                        }] for field, msgs in exception.message_dict.items()
                    }
                }
                return ErrorResponse.create_error_response(
                    error_detail=formatted_error,
                    api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT
                )
            else:
                # Single error message
                formatted_error = {
                    'message': ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT],
                    'code': 'invalid_input',
                    ErrorResponseFields.FIELD_ERRORS: {
                        ErrorResponseFields.DETAILS: [{
                            'message': str(exception.messages[0] if exception.messages else exception),
                            'code': ErrorResponseFields.DefaultFieldValidationValues.NonDbIntegrityError.CODE
                        }]
                    }
                }
                return ErrorResponse.create_error_response(
                    error_detail=formatted_error, api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT)

        # Generic validation error
        error_detail = {'message': str(exception), 'code': ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT.name.lower()}
        return ErrorResponse.create_error_response(
            error_detail=error_detail, api_error_code=ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT)

    @staticmethod
    def _from_method_not_allowed_exception(exception: MethodNotAllowed) -> JsonResponse:
        detail = exception.detail
        message = detail['detail'] if isinstance(detail, dict) and 'detail' in detail else exception.default_detail
        return ErrorResponse.create_error_response(error_detail={'message': message, 'code': 'method_not_allowed'},
                                                   api_error_code=ApiErrorCodeNumeric.VALIDATION_METHOD_NOT_ALLOWED)

    @staticmethod
    def handle_exception(exc: Exception) -> JsonResponse:
        """
        Routes different types of exceptions to their appropriate handlers.
        """
        if isinstance(exc, DrfValidationError):
            converted = AppValidationException._detect_and_convert_from_drf_exception(exc)
            if converted:
                exc = converted
            return ErrorResponse._from_validation_error(exc)
        elif isinstance(exc, IntegrityError):
            return ErrorResponse._from_unhandled_integrity_error(exc)
        elif isinstance(exc, (InvalidToken, NotAuthenticated)):
            return ErrorResponse._from_invalid_jwt_token(exc)
        elif isinstance(exc, ParseError):
            return ErrorResponse._from_content_type_exception(exc)
        elif isinstance(exc, UnsupportedMediaType):
            return ErrorResponse._from_unsupported_media_type_exception(exc)
        elif isinstance(exc, MethodNotAllowed):
            return ErrorResponse._from_method_not_allowed_exception(exc)
        else:
            return ErrorResponse._from_unhandled_exception(exc)
