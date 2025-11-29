import logging
import traceback
from time import time

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('exceptions')

    def __call__(self, request):
        start_time = time()
        request_id = getattr(request, 'request_id', 'unknown')
        self.logger.info(
            f"[{request_id}] Incoming Request: {request.method} {request.path} {request.META.get('REMOTE_ADDR')}")

        response = self.get_response(request)

        processing_time = time() - start_time
        self.logger.info(
            f"[{request_id}] Response: {response.status_code} {response.reason_phrase} (took {processing_time:.3f}s)")
        return response

    def process_exception(self, request, exception):
        request_id = getattr(request, 'request_id', 'unknown')
        try:
            exc_str = str(exception)
        except Exception:
            exc_str = f"{type(exception).__name__}: <unable to stringify exception>"
        self.logger.error(f"[{request_id}] Exception: {type(exception).__name__} - {exc_str}")
        try:
            self.logger.error('\n'.join(traceback.format_exception(
                type(exception), exception, exception.__traceback__)))
        except Exception as traceback_error:
            self.logger.error(
                f"[{request_id}] Error formatting traceback: {type(traceback_error).__name__} - {str(traceback_error)}")

        try:
            response = ErrorResponse.handle_exception(exception)
            self.logger.error(f"[{request_id}] Error Response: {response.status_code} {response.reason_phrase}")
        except Exception as e:
            try:
                e_str = str(e)
            except Exception:
                e_str = f"{type(e).__name__}: <unable to stringify exception>"
            self.logger.error(f"[{request_id}] Error in ErrorResponse Handling: {type(e).__name__} - {e_str}")
            try:
                self.logger.error('\n'.join(traceback.format_exception(type(e), e, e.__traceback__)))
            except Exception as traceback_error:
                self.logger.error(
                    f"[{request_id}] Error formatting traceback: {type(traceback_error).__name__} - {str(traceback_error)}")

        return None
