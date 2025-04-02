
from rest_framework import status

from bodzify_api.exception.validation.app.AppValidationExceptionFields import AppValidationErrorFields
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class ErrorResponseFields:

    CODE = 'code'  # Global error code
    MESSAGE = 'message'  # Used for general error messages
    SUCCESS = 'success'  # Indicates if the operation was successful
    DETAILS = 'details'  # list of detailed error information
    FIELD_ERRORS = 'fieldErrors'  # Used for field-specific error messages

    class FieldErrors:
        FIELD = AppValidationErrorFields.FIELD
        MESSAGE = 'message'
        CODE = 'code'

    class DefaultFieldValidationValues:
        class DbIntegrityError:
            MESSAGE = 'Field validation error due to database integrity'
            CODE = FieldValidationErrorCode.DB_INTEGRITY_ERROR

        class NonDbIntegrityError:
            MESSAGE = 'Field validation error'
            CODE = FieldValidationErrorCode.DEFAULT

    MESSAGES = {
        # Authentication errors
        ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS: "Invalid authentication credentials",
        ApiErrorCodeNumeric.AUTH_TOKEN_EXPIRED: "Authentication token has expired",
        ApiErrorCodeNumeric.AUTH_TOKEN_INVALID: "Invalid authentication token",
        ApiErrorCodeNumeric.AUTH_INSUFFICIENT_PERMISSIONS: "Insufficient permissions for this operation",

        # Validation errors
        ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT: "One or more fields contain invalid data. Please check the error details for specific validation requirements",
        ApiErrorCodeNumeric.VALIDATION_UNSUPPORTED_MEDIA_TYPE: "Unsupported media type. Please check the Content-Type header",
        ApiErrorCodeNumeric.VALIDATION_METHOD_NOT_ALLOWED: "The HTTP method is not allowed for this endpoint",

        # Resource errors
        ApiErrorCodeNumeric.RESOURCE_NOT_FOUND: "The requested resource could not be found",
        ApiErrorCodeNumeric.RESOURCE_ALREADY_EXISTS: "Resource already exists",
        ApiErrorCodeNumeric.RESOURCE_FILE_NOT_FOUND: "The requested file could not be found",
        ApiErrorCodeNumeric.RESOURCE_INVALID_STATE: "Resource is in an invalid state for this operation",

        # Business errors
        ApiErrorCodeNumeric.BUSINESS_INVALID_OPERATION: "The requested operation cannot be performed",
        ApiErrorCodeNumeric.BUSINESS_DEPENDENCY_ERROR: "Operation failed due to dependency issues",
        ApiErrorCodeNumeric.BUSINESS_LIMIT_EXCEEDED: "Operation limit has been exceeded",

        # External Service errors
        ApiErrorCodeNumeric.EXTERNAL_SERVICE_ERROR: "External service encountered an error",
        ApiErrorCodeNumeric.EXTERNAL_SERVICE_TIMEOUT: "External service request timed out",
        ApiErrorCodeNumeric.EXTERNAL_SERVICE_UNAVAILABLE: "External service is temporarily unavailable",

        # Security (6000-6999)
        ApiErrorCodeNumeric.SECURITY_ERROR: "Security error",

        # System errors
        ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR: "An internal system error occurred",
        ApiErrorCodeNumeric.SYSTEM_NOT_IMPLEMENTED: "An internal system error occurred",
        ApiErrorCodeNumeric.SYSTEM_SERVICE_UNAVAILABLE: "An internal system error occurred",
        ApiErrorCodeNumeric.SYSTEM_SERIALIZER_NOT_DEFINED: "An internal system error occurred",
    }

    STATUS_MESSAGES = {
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        status.HTTP_403_FORBIDDEN: "Forbidden",
        status.HTTP_404_NOT_FOUND: "Not Found",
        status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Allowed",
        status.HTTP_409_CONFLICT: "Conflict",
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: "Unsupported Media Type",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "Unprocessable Entity",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        status.HTTP_501_NOT_IMPLEMENTED: "Not Implemented",
        status.HTTP_502_BAD_GATEWAY: "Bad Gateway",
        status.HTTP_503_SERVICE_UNAVAILABLE: "Service Unavailable",
        status.HTTP_504_GATEWAY_TIMEOUT: "Gateway Timeout"
    }

    ERROR_TO_HTTP_STATUS = {
        # Auth errors -> 401/403
        ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
        ApiErrorCodeNumeric.AUTH_TOKEN_EXPIRED: status.HTTP_401_UNAUTHORIZED,
        ApiErrorCodeNumeric.AUTH_TOKEN_INVALID: status.HTTP_401_UNAUTHORIZED,
        ApiErrorCodeNumeric.AUTH_INSUFFICIENT_PERMISSIONS: status.HTTP_403_FORBIDDEN,

        # Validation errors -> 400
        ApiErrorCodeNumeric.VALIDATION_INVALID_INPUT: status.HTTP_400_BAD_REQUEST,
        ApiErrorCodeNumeric.VALIDATION_MISSING_FIELD: status.HTTP_400_BAD_REQUEST,
        ApiErrorCodeNumeric.VALIDATION_INVALID_FORMAT: status.HTTP_400_BAD_REQUEST,
        ApiErrorCodeNumeric.VALIDATION_INVALID_UUID: status.HTTP_400_BAD_REQUEST,
        ApiErrorCodeNumeric.VALIDATION_INTEGRITY_ERROR: status.HTTP_400_BAD_REQUEST,
        ApiErrorCodeNumeric.VALIDATION_UNSUPPORTED_MEDIA_TYPE: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        ApiErrorCodeNumeric.VALIDATION_METHOD_NOT_ALLOWED: status.HTTP_405_METHOD_NOT_ALLOWED,

        # Resource errors -> 404/409
        ApiErrorCodeNumeric.RESOURCE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiErrorCodeNumeric.RESOURCE_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        ApiErrorCodeNumeric.RESOURCE_FILE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiErrorCodeNumeric.RESOURCE_INVALID_STATE: status.HTTP_409_CONFLICT,

        # Business Logic errors -> 422
        ApiErrorCodeNumeric.BUSINESS_INVALID_OPERATION: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ApiErrorCodeNumeric.BUSINESS_DEPENDENCY_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ApiErrorCodeNumeric.BUSINESS_LIMIT_EXCEEDED: status.HTTP_422_UNPROCESSABLE_ENTITY,

        # External Service errors -> 502/504
        ApiErrorCodeNumeric.EXTERNAL_SERVICE_ERROR: status.HTTP_502_BAD_GATEWAY,
        ApiErrorCodeNumeric.EXTERNAL_SERVICE_TIMEOUT: status.HTTP_504_GATEWAY_TIMEOUT,
        ApiErrorCodeNumeric.EXTERNAL_SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,

        # System/Internal errors -> 500
        ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ApiErrorCodeNumeric.SYSTEM_NOT_IMPLEMENTED: status.HTTP_501_NOT_IMPLEMENTED,
        ApiErrorCodeNumeric.SYSTEM_SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
    }
