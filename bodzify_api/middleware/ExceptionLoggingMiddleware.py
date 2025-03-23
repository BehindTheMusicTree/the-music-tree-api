import logging
import traceback
from django.core.exceptions import DisallowedHost

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the exception first
        logger = logging.getLogger('exceptions')
        logger.error(type(exception))
        logger.error(exception)
        if exception.__traceback__:
            logger.error('\n'.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))
        else:
            logger.error('No traceback available for this exception')
        # Handle DisallowedHost directly in middleware as recommended by the docstring
        if isinstance(exception, DisallowedHost):
            return ErrorResponse.handle_exception(exception)
