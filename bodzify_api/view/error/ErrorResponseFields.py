class ErrorResponseFields:
    """Constants for API response field names."""
    
    # Response structure fields
    MESSAGE = 'message'  # Main message field used across all responses
    CODE = 'code'  # Error code field used across all responses
    SUCCESS = 'success'  # Indicates if the request was successful
    DETAILS = 'details'  # List of detailed error information
    DETAIL = 'detail'  # Used for single error messages