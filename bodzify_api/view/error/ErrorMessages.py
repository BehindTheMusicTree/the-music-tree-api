from bodzify_api.view.error.ErrorCode import ErrorCode


class AppErrorMessages:

    MESSAGES = {
        # Authentication errors
        ErrorCode.AUTH_INVALID_CREDENTIALS: "Invalid authentication credentials",
        ErrorCode.AUTH_TOKEN_EXPIRED: "Authentication token has expired",
        ErrorCode.AUTH_TOKEN_INVALID: "Invalid authentication token",
        ErrorCode.AUTH_INSUFFICIENT_PERMISSIONS: "Insufficient permissions for this operation",

        # Validation errors
        ErrorCode.VALIDATION_INVALID_INPUT: "The provided parameters are invalid",
        ErrorCode.VALIDATION_MISSING_FIELD: "Required field is missing",
        ErrorCode.VALIDATION_INVALID_FORMAT: "Invalid data format",
        ErrorCode.VALIDATION_INVALID_UUID: "The provided identifier is invalid",
        ErrorCode.VALIDATION_INTEGRITY_ERROR: "The request contains invalid or conflicting data",

        # Resource errors
        ErrorCode.RESOURCE_NOT_FOUND: "The requested resource could not be found",
        ErrorCode.RESOURCE_ALREADY_EXISTS: "Resource already exists",
        ErrorCode.RESOURCE_FILE_NOT_FOUND: "The requested file could not be found",
        ErrorCode.RESOURCE_INVALID_STATE: "Resource is in an invalid state for this operation",

        # Business errors
        ErrorCode.BUSINESS_INVALID_OPERATION: "The requested operation cannot be performed",
        ErrorCode.BUSINESS_DEPENDENCY_ERROR: "Operation failed due to dependency issues",
        ErrorCode.BUSINESS_LIMIT_EXCEEDED: "Operation limit has been exceeded",

        # External Service errors
        ErrorCode.EXTERNAL_SERVICE_ERROR: "External service encountered an error",
        ErrorCode.EXTERNAL_SERVICE_TIMEOUT: "External service request timed out",
        ErrorCode.EXTERNAL_SERVICE_UNAVAILABLE: "External service is temporarily unavailable",

        # System errors
        ErrorCode.SYSTEM_INTERNAL_ERROR: "An internal system error occurred",
        ErrorCode.SYSTEM_NOT_IMPLEMENTED: "An internal system error occurred",
        ErrorCode.SYSTEM_SERVICE_UNAVAILABLE: "An internal system error occurred",
        ErrorCode.SYSTEM_SERIALIZER_NOT_DEFINED: "An internal system error occurred",
    }
