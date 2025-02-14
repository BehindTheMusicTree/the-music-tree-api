from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class ValidationErrorFields:
    """Constants for validation error field names and messages."""
    
    # Validation structure fields
    MESSAGE = ErrorResponseFields.MESSAGE  # Reference to main response field
    CODE = ErrorResponseFields.CODE  # Reference to main response field
    FIELD_ERRORS = 'fieldErrors'
    
    # Common validation error codes
    VALIDATION_ERROR = 'validation_error'
    BLANK_ERROR = 'blank'
    INVALID_ERROR = 'invalid'