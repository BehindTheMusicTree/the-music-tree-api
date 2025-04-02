import logging
import traceback
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import HttpRequest

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class HostValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('exceptions')

    def __call__(self, request: HttpRequest):
        try:
            host = request.get_host()
            if host not in settings.ALLOWED_HOSTS and '*' not in settings.ALLOWED_HOSTS:
                self.logger.error(type(DisallowedHost))
                self.logger.error(f"Invalid HTTP_HOST header: '{host}'")
                if settings.DEBUG:
                    self.logger.error('\n'.join(traceback.format_stack()))
                return ErrorResponse.handle_exception(DisallowedHost(host))
            return self.get_response(request)
        except DisallowedHost as exc:
            self.logger.error(type(exc))
            self.logger.error(str(exc))
            if exc.__traceback__:
                self.logger.error('\n'.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
            return ErrorResponse.handle_exception(exc)
