import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logMessage = f"Incoming Request: {request.method} {request.path}"
        requestLogger = logging.getLogger('request')
        requestLogger.info(logMessage)
        requestDebugLogger = logging.getLogger('django.request')
        requestDebugLogger.info(logMessage)

        response = self.get_response(request)
        return response

class Middleware1:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response1: {response.status_code}")
        return response

class Middleware2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response2: {response.status_code}")
        return response

class Middleware3:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response3: {response.status_code}")
        return response

class Middleware4:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response4: {response.status_code}")
        return response

class Middleware5:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response5: {response.status_code}")
        return response

class Middleware6:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response6: {response.status_code}")
        return response

class Middleware7:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        response = self.get_response(request)
        logger.info(f"Outgoing Response7: {response.status_code}")
        return response