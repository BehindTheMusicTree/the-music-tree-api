from bodzify_api.view.error.ErrorCode import ErrorCode


class AppErrorMessages:
    MESSAGES = {
        ErrorCode.VALIDATION_INTEGRITY_ERROR: "There is an issue with the object sent",
        ErrorCode.VALIDATION_INVALID_UUID: "A valid UUID is required.",
        ErrorCode.SYSTEM_NOT_IMPLEMENTED: "Service not defined in viewset",
        ErrorCode.BUSINESS_INVALID_OPERATION: "Pagination not set",
        ErrorCode.RESOURCE_FILE_NOT_FOUND: "The requested file could not be found",
        ErrorCode.VALIDATION_INVALID_INPUT: "Invalid query parameters provided",
        ErrorCode.SYSTEM_NOT_IMPLEMENTED: {
            'detailed': "detailed_serializer_class not defined in viewset",
            'simple': "simple_serializer_class not defined in viewset",
            'create': "create_serializer_class not defined in viewset",
            'update': "update_serializer_class not defined in viewset"
        }
    }
