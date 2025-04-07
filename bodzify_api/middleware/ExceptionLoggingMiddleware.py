import logging
import traceback

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('exceptions')

    def __call__(self, request):
        self.logger.info(f"=== Request Start ===")
        self.logger.info(f"Path: {request.path}")
        self.logger.info(f"Method: {request.method}")
        self.logger.info(f"Headers: {dict(request.headers)}")
        if request.body:
            try:
                self.logger.info(f"Body: {request.body.decode('utf-8')}")
            except UnicodeDecodeError:
                self.logger.info("Body: <binary data>")

        response = self.get_response(request)

        self.logger.info(f"=== Request End ===")
        self.logger.info(f"Status: {response.status_code}")
        self.logger.info(f"Content-Type: {response.get('Content-Type', '')}")
        return response

    def process_exception(self, request, exception):
        self.logger.error("=== Exception Handling Start ===")
        self.logger.error(f"Request ID: {getattr(request, 'request_id', 'unknown')}")
        self.logger.error(f"Exception Type: {type(exception)}")
        self.logger.error(f"Exception Message: {str(exception)}")
        self.logger.error(f"Request Path: {request.path}")
        self.logger.error(f"Request Method: {request.method}")
        self.logger.error(f"Request Headers: {dict(request.headers)}")

        if exception.__traceback__:
            self.logger.error("Full Traceback:")
            self.logger.error('\n'.join(traceback.format_exception(
                type(exception), exception, exception.__traceback__)))
        else:
            self.logger.error('No traceback available for this exception')

        try:
            self.logger.error("=== ErrorResponse Handling ===")
            response = ErrorResponse.handle_exception(exception)
            self.logger.error(f"Generated Status Code: {response.status_code}")
            self.logger.error(f"Generated Content: {response.content.decode('utf-8')}")
            self.logger.error(f"Response Headers: {dict(response.headers)}")
        except Exception as e:
            self.logger.error("=== Error in ErrorResponse Handling ===")
            self.logger.error(f"Error Type: {type(e)}")
            self.logger.error(f"Error Message: {str(e)}")
            if e.__traceback__:
                self.logger.error("Error Traceback:")
                self.logger.error('\n'.join(traceback.format_exception(type(e), e, e.__traceback__)))

        self.logger.error("=== Exception Handling End ===")
        return None
