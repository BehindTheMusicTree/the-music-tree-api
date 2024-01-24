import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request
        logger = logging.getLogger('request')
        logger.info(f"Incoming Request: {request.method} {request.path}")

        response = self.get_response(request)
        return response