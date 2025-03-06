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
    return ErrorResponse.handle_exception(exc)
