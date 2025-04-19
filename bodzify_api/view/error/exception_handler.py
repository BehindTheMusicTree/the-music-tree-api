
from django.http.response import Http404
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import (
    NotAuthenticated, ValidationError, MethodNotAllowed, PermissionDenied, AuthenticationFailed
)

from bodzify_api.view.error.ErrorResponse import ErrorResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that integrates with our ErrorResponse system.
    In debug mode, it falls back to Django's default HTML traceback.
    In production, it uses our custom error response format.

    Important Note on Middleware Exceptions:
    --------------------------------------
    This handler only processes exceptions from DRF views and viewsets. Exceptions raised
    in middleware are handled differently because they occur before reaching DRF's
    exception handling system.

    For middleware exceptions:
    1. Do not raise exceptions in middleware expecting them to be caught here
    2. Instead, handle exceptions directly in the middleware using ErrorResponse
    3. Return a JsonResponse instead of raising

    Example middleware pattern:
        class YourMiddleware:
            def handle_error(self, exc):
                return ErrorResponse.handle_exception(exc)

            def __call__(self, request):
                if error_condition:
                    return self.handle_error(SomeException("error message"))
                return self.get_response(request)

    This ensures consistent error handling and formatting across the application,
    whether the error occurs in middleware or views.

    Args:
        exc: The caught exception
        context: Additional context (includes the request)

    Returns:
        Response object with error details in production,
        None in debug mode to let Django's default handler show the traceback page
    """

    print('exception_handler', exc)
    if settings.DEBUG and not isinstance(
        exc,
        (ValidationError, InvalidToken, NotAuthenticated, AuthenticationFailed, MethodNotAllowed, Http404,
         PermissionDenied)):
        # Return None to let Django's default handler show the HTML traceback page
        return None

    # In production, use our custom error response
    return ErrorResponse.handle_exception(exc)
