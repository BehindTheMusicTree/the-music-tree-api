import logging
import uuid
from time import time

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request')

    def __call__(self, request):
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        request.request_id = request_id

        start_time = time()
        self.logger.info(
            f"[{request_id}] Incoming Request: {request.method} {request.path} {request.META.get('REMOTE_ADDR')}")

        response = self.get_response(request)

        processing_time = time() - start_time
        self.logger.info(
            f"[{request_id}] Response: {response.status_code} {response.reason_phrase} (took {processing_time:.3f}s)")
        return response

    def process_exception(self, request, exception):
        request_id = getattr(request, 'request_id', 'unknown')
        self.logger.error(f"[{request_id}] Exception: {type(exception).__name__} - {str(exception)}")
        self.logger.error('\n'.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

        try:
            response = ErrorResponse.handle_exception(exception)
            self.logger.error(f"[{request_id}] Error Response: {response.status_code} {response.reason_phrase}")
        except Exception as e:
            self.logger.error(f"[{request_id}] Error in ErrorResponse Handling: {type(e).__name__} - {str(e)}")
            self.logger.error('\n'.join(traceback.format_exception(type(e), e, e.__traceback__)))

        return None
