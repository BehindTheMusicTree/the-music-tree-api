import logging
import uuid
import time


def _generate_log_about_headers(request):
    logMessage = "Headers: "
    for header in request.headers:
        logMessage += f"{header}: {request.headers[header]} "
    return logMessage


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requestLogger = logging.getLogger('request')
        requestDebugLogger = logging.getLogger('django.request')

        # Generate a unique request ID and start time
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        start_time = time.time()

        # Log request details
        logMessage = f"[{request_id}] Incoming Request: {request.method} {request.path} {request.META['REMOTE_ADDR']} "
        requestLogger.info(logMessage)
        requestDebugLogger.info(logMessage)
        requestDebugLogger.info(_generate_log_about_headers(request))

        # Log request body for non-GET requests
        if request.method != 'GET' and request.body:
            try:
                body = request.body.decode('utf-8')
                if body:
                    requestDebugLogger.info(f"[{request_id}] Request Body: {body}")
            except UnicodeDecodeError:
                requestDebugLogger.info(f"[{request_id}] Request Body: <binary data>")

        try:
            response = self.get_response(request)
            duration = time.time() - start_time

            # Log response details
            responseCodeMessage = f"[{request_id}] Response: {response.status_code} {response.reason_phrase} (took {duration:.3f}s)"
            requestLogger.info(responseCodeMessage)
            requestDebugLogger.info(responseCodeMessage)

            # Log response body for non-streaming responses
            if hasattr(response, 'content') and not getattr(response, 'streaming', False):
                try:
                    content = response.content.decode('utf-8')
                    if content:
                        requestDebugLogger.info(f"[{request_id}] Response Body: {content}")
                except UnicodeDecodeError:
                    requestDebugLogger.info(f"[{request_id}] Response Body: <binary data>")

            return response

        except Exception as e:
            duration = time.time() - start_time
            error_message = f"[{request_id}] Error: {str(e)} (took {duration:.3f}s)"
            requestLogger.error(error_message)
            requestDebugLogger.error(error_message)
            raise
