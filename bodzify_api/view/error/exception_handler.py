from rest_framework.views import exception_handler

from bodzify_api.view.error.ErrorResponse import ErrorResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that integrates with our ErrorResponse system.
    This ensures all exceptions, including validation exceptions, go through our error handling logic.
    
    Args:
        exc: The caught exception
        context: Additional context (includes the request)
        
    Returns:
        Response object with error details
    """
    # First try default DRF exception handling
    response = exception_handler(exc, context)
    
    # If DRF didn't handle it or we want to override its handling,
    # use our ErrorResponse handler
    if response is None:
        return ErrorResponse.handle_exception(exc)
    
    return response