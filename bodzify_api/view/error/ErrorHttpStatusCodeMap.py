from rest_framework import status

from bodzify_api.view.error.ApiErrorCode import ApiErrorCode


class ErrorHTTPStatusCodeMap:
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
