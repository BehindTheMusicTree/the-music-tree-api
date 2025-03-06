from django.conf import settings
from bodzify_api.view.error.ErrorResponse import ErrorResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that integrates with our ErrorResponse system.
    In debug mode, it falls back to Django's default HTML traceback.
    In production, it uses our custom error response format.

    Args:
        exc: The caught exception
        context: Additional context (includes the request)

    Returns:
        Response object with error details in production,
        None in debug mode to let Django's default handler show the traceback page
    """
    if settings.DEBUG:
        # Return None to let Django's default handler show the HTML traceback page
        return None

    # In production, use our custom error response
    return ErrorResponse.handle_exception(exc)
