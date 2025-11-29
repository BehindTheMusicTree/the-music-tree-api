import logging
import traceback
import uuid
import time

from bodzify_api.view.error.ErrorResponse import ErrorResponse


def _generate_log_about_headers(request):
    logMessage = "Headers: "
    for header in request.headers:
        logMessage += f"{header}: {request.headers[header]} "
    return logMessage


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.requestLogger = logging.getLogger('request')
        self.requestDebugLogger = logging.getLogger('django.request')

    def __call__(self, request):
        # Generate a unique request ID and start time
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        start_time = time.time()

        # Log request details
        logMessage = f"[{request_id}] Incoming Request: {request.method} {request.path} {request.META.get('REMOTE_ADDR')} "
        self.requestLogger.info(logMessage)
        self.requestDebugLogger.info(logMessage)
        self.requestDebugLogger.info(_generate_log_about_headers(request))

        # Log request body for non-GET requests
        if request.method != 'GET':
            try:
                # Try to get the body from the request attribute first (set by other middleware)
                body = getattr(request, '_body', None)
                if body is None:
                    # If not set, try to read the body directly
                    body = request.body
                    # Store the body in a request attribute for other middleware
                    request._body = body

                if body:
                    try:
                        body_str = body.decode('utf-8')
                        if body_str:
                            self.requestDebugLogger.info(f"[{request_id}] Request Body: {body_str}")
                    except UnicodeDecodeError:
                        self.requestDebugLogger.info(f"[{request_id}] Request Body: <binary data>")
            except Exception as e:
                # Log the error but don't fail the request
                self.requestDebugLogger.error(f"[{request_id}] Error reading request body: {str(e)}")

        try:
            self.requestDebugLogger.info(f"[{request_id}] DEBUG: About to call get_response")
            response = self.get_response(request)
            duration = time.time() - start_time

            # Log response details
            responseCodeMessage = f"[{request_id}] Response: {response.status_code} {response.reason_phrase} (took {duration:.3f}s)"
            self.requestLogger.info(responseCodeMessage)
            self.requestDebugLogger.info(responseCodeMessage)

            # Special logging for PUT requests to genres
            if request.method == 'PUT' and '/genres/' in request.path:
                self.requestDebugLogger.info(
                    f"[{request_id}] DEBUG: PUT request to genres completed with status {response.status_code}")

            # Log response body for non-streaming responses
            if hasattr(response, 'content') and not getattr(response, 'streaming', False):
                try:
                    content = response.content.decode('utf-8')
                    if content:
                        self.requestDebugLogger.info(f"[{request_id}] Response Body: {content}")
                except UnicodeDecodeError:
                    self.requestDebugLogger.info(f"[{request_id}] Response Body: <binary data>")

            return response

        except Exception as e:
            duration = time.time() - start_time
            try:
                error_str = str(e)
            except Exception:
                error_str = f"{type(e).__name__}: <unable to stringify exception>"
            error_message = f"[{request_id}] Error: {error_str} (took {duration:.3f}s)"
            try:
                self.requestLogger.error(error_message)
                self.requestDebugLogger.error(error_message)
            except Exception as log_error:
                self.requestDebugLogger.error(f"[{request_id}] Error logging exception: {type(log_error).__name__}: {str(log_error)}")

            # Special logging for PUT requests to genres
            if request.method == 'PUT' and '/genres/' in request.path:
                try:
                    exc_str = str(e)
                except Exception:
                    exc_str = f"{type(e).__name__}: <unable to stringify exception>"
                try:
                    self.requestDebugLogger.error(
                        f"[{request_id}] DEBUG: PUT request to genres failed with exception: {type(e).__name__}: {exc_str}")
                    import traceback
                    self.requestDebugLogger.error(f"[{request_id}] DEBUG: Exception traceback: {traceback.format_exc()}")
                except Exception as log_error:
                    self.requestDebugLogger.error(f"[{request_id}] Error in detailed logging: {type(log_error).__name__}: {str(log_error)}")

            raise

    def process_exception(self, request, exception):
        request_id = getattr(request, 'request_id', 'unknown')
        try:
            exc_str = str(exception)
        except Exception:
            exc_str = f"{type(exception).__name__}: <unable to stringify exception>"
        try:
            self.requestLogger.error(f"[{request_id}] Exception: {type(exception).__name__} - {exc_str}")
            self.requestLogger.error('\n'.join(traceback.format_exception(
                type(exception), exception, exception.__traceback__)))
        except Exception as log_error:
            self.requestDebugLogger.error(f"[{request_id}] Error logging exception details: {type(log_error).__name__}: {str(log_error)}")

        try:
            response = ErrorResponse.handle_exception(exception)
            self.requestLogger.error(f"[{request_id}] Error Response: {response.status_code} {response.reason_phrase}")
        except Exception as e:
            try:
                e_str = str(e)
            except Exception:
                e_str = f"{type(e).__name__}: <unable to stringify exception>"
            try:
                self.requestLogger.error(f"[{request_id}] Error in ErrorResponse Handling: {type(e).__name__} - {e_str}")
                self.requestLogger.error('\n'.join(traceback.format_exception(type(e), e, e.__traceback__)))
            except Exception as log_error:
                self.requestDebugLogger.error(f"[{request_id}] Error logging ErrorResponse handling error: {type(log_error).__name__}: {str(log_error)}")

        return None
