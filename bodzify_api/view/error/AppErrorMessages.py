from bodzify_api.view.error.ApiErrorCode import ApiErrorCode


class AppErrorMessages:

    MESSAGES = {
        # Authentication errors
        ApiErrorCode.AUTH_INVALID_CREDENTIALS: "Invalid authentication credentials",
        ApiErrorCode.AUTH_TOKEN_EXPIRED: "Authentication token has expired",
        ApiErrorCode.AUTH_TOKEN_INVALID: "Invalid authentication token",
        ApiErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: "Insufficient permissions for this operation",

        # Validation errors
        ApiErrorCode.VALIDATION_INVALID_INPUT: "The provided parameters are invalid",
        ApiErrorCode.VALIDATION_MISSING_FIELD: "Required field is missing",
        ApiErrorCode.VALIDATION_INVALID_FORMAT: "Invalid data format",
        ApiErrorCode.VALIDATION_INVALID_UUID: "The provided identifier is invalid",
        ApiErrorCode.VALIDATION_INTEGRITY_ERROR: "The request contains invalid or conflicting data",

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
