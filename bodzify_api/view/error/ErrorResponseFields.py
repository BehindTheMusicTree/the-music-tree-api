
from locale import CODESET
from rest_framework import status

from bodzify_api.validator.AppValidationErrorFields import AppValidationErrorFields
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ApiErrorCode import ApiErrorCode


class ErrorResponseFields:

    CODE = 'code'  # Global error code
    MESSAGE = 'message'  # Used for general error messages
    SUCCESS = 'success'  # Indicates if the operation was successful
    DETAILS = 'details'  # List of detailed error information
    DETAIL = 'detail'  # Used for single error messages
    FIELD_ERRORS = 'field_errors'  # Used for field-specific error messages

    class FieldErrors:
        FIELD = AppValidationErrorFields.FIELD
        MESSAGE = AppValidationErrorFields.MESSAGE
        CODE = AppValidationErrorFields.CODE

    class DefaultFieldValidationValues:
        class DbIntegrityError:
            MESSAGE = 'Field validation error due to database integrity'
            CODE = FieldValidationErrorCode.DB_INTEGRITY_ERROR.value

        class NonDbIntegrityError:
            MESSAGE = 'Field validation error'
            CODE = FieldValidationErrorCode.DEFAULT.value

    MESSAGES = {
        # Authentication errors
        ApiErrorCode.AUTH_INVALID_CREDENTIALS: "Invalid authentication credentials",
        ApiErrorCode.AUTH_TOKEN_EXPIRED: "Authentication token has expired",
        ApiErrorCode.AUTH_TOKEN_INVALID: "Invalid authentication token",
        ApiErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: "Insufficient permissions for this operation",

        # Validation errors
        ApiErrorCode.VALIDATION_INVALID_INPUT: "The provided data is invalid",

        # Resource errors
        ApiErrorCode.RESOURCE_NOT_FOUND: "The requested resource could not be found",
        ApiErrorCode.RESOURCE_ALREADY_EXISTS: "Resource already exists",
        ApiErrorCode.RESOURCE_FILE_NOT_FOUND: "The requested file could not be found",
        ApiErrorCode.RESOURCE_INVALID_STATE: "Resource is in an invalid state for this operation",

        # Business errors
        ApiErrorCode.BUSINESS_INVALID_OPERATION: "The requested operation cannot be performed",
        ApiErrorCode.BUSINESS_DEPENDENCY_ERROR: "Operation failed due to dependency issues",
        ApiErrorCode.BUSINESS_LIMIT_EXCEEDED: "Operation limit has been exceeded",

        # External Service errors
        ApiErrorCode.EXTERNAL_SERVICE_ERROR: "External service encountered an error",
        ApiErrorCode.EXTERNAL_SERVICE_TIMEOUT: "External service request timed out",
        ApiErrorCode.EXTERNAL_SERVICE_UNAVAILABLE: "External service is temporarily unavailable",

        # System errors
        ApiErrorCode.SYSTEM_INTERNAL_ERROR: "An internal system error occurred",
        ApiErrorCode.SYSTEM_NOT_IMPLEMENTED: "An internal system error occurred",
        ApiErrorCode.SYSTEM_SERVICE_UNAVAILABLE: "An internal system error occurred",
        ApiErrorCode.SYSTEM_SERIALIZER_NOT_DEFINED: "An internal system error occurred",
    }

    STATUS_MESSAGES = {
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        status.HTTP_403_FORBIDDEN: "Forbidden",
        status.HTTP_404_NOT_FOUND: "Not Found",
        status.HTTP_409_CONFLICT: "Conflict",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "Unprocessable Entity",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        status.HTTP_501_NOT_IMPLEMENTED: "Not Implemented",
        status.HTTP_502_BAD_GATEWAY: "Bad Gateway",
        status.HTTP_503_SERVICE_UNAVAILABLE: "Service Unavailable",
        status.HTTP_504_GATEWAY_TIMEOUT: "Gateway Timeout"
    }

    ERROR_TO_HTTP_STATUS = {
        # Auth errors -> 401/403
        ApiErrorCode.AUTH_INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
        ApiErrorCode.AUTH_TOKEN_EXPIRED: status.HTTP_401_UNAUTHORIZED,
        ApiErrorCode.AUTH_TOKEN_INVALID: status.HTTP_401_UNAUTHORIZED,
        ApiErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: status.HTTP_403_FORBIDDEN,

        # Validation errors -> 400
        ApiErrorCode.VALIDATION_INVALID_INPUT: status.HTTP_400_BAD_REQUEST,
        ApiErrorCode.VALIDATION_MISSING_FIELD: status.HTTP_400_BAD_REQUEST,
        ApiErrorCode.VALIDATION_INVALID_FORMAT: status.HTTP_400_BAD_REQUEST,
        ApiErrorCode.VALIDATION_INVALID_UUID: status.HTTP_400_BAD_REQUEST,
        ApiErrorCode.VALIDATION_INTEGRITY_ERROR: status.HTTP_400_BAD_REQUEST,

        # Resource errors -> 404/409
        ApiErrorCode.RESOURCE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiErrorCode.RESOURCE_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        ApiErrorCode.RESOURCE_FILE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiErrorCode.RESOURCE_INVALID_STATE: status.HTTP_409_CONFLICT,

        # Business Logic errors -> 422
        ApiErrorCode.BUSINESS_INVALID_OPERATION: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ApiErrorCode.BUSINESS_DEPENDENCY_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ApiErrorCode.BUSINESS_LIMIT_EXCEEDED: status.HTTP_422_UNPROCESSABLE_ENTITY,

        # External Service errors -> 502/504
        ApiErrorCode.EXTERNAL_SERVICE_ERROR: status.HTTP_502_BAD_GATEWAY,
        ApiErrorCode.EXTERNAL_SERVICE_TIMEOUT: status.HTTP_504_GATEWAY_TIMEOUT,
        ApiErrorCode.EXTERNAL_SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,

        # System/Internal errors -> 500
        ApiErrorCode.SYSTEM_INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ApiErrorCode.SYSTEM_NOT_IMPLEMENTED: status.HTTP_501_NOT_IMPLEMENTED,
        ApiErrorCode.SYSTEM_SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
    }
