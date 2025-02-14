class ErrorResponseFields:
    """Constants for error response field names and messages."""
    
    # Response structure fields
    MESSAGE = 'message'
    FIELD_ERRORS = 'fieldErrors'
    CODE = 'code'
    SUCCESS = 'success'
    DETAILS = 'details'
    DETAIL = 'detail'  # Used for single error messages
    
    # Common error messages
    VALIDATION_FAILED = 'Validation failed'
    INTERNAL_ERROR = 'An internal error occurred'
    BAD_REQUEST = 'Bad Request'

    # Common error codes
    VALIDATION_ERROR = 'validation_error'
    BLANK_ERROR = 'blank'
    INVALID_ERROR = 'invalid'