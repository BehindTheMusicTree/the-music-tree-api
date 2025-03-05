from json.decoder import JSONDecodeError
from typing import Any

from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.exceptions import ParseError

from bodzify_api.view.error.ApiErrorCode import ApiErrorCode
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> JsonResponse | None:
    """
    Custom exception handler that formats JSON parse errors to match our API's error format.
    Falls back to default handling for other exceptions.
    """
    if isinstance(exc, (JSONDecodeError, ParseError)):
        return ErrorResponse.create_error_response(
            error_detail={
                ErrorResponseFields.MESSAGE: str(exc),
            },
            api_error_code=ApiErrorCode.VALIDATION_INVALID_INPUT
        )

    # Use DRF's default exception handler for other exceptions
    response = exception_handler(exc, context)
    if response is None:
        return None

    # Convert DRF Response to JsonResponse while preserving status and content
    return JsonResponse(data=response.data, status=response.status_code, safe=False)
