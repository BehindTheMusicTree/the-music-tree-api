import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('request')
        logger.info(f"Incoming Request: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware1:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request1: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request2: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware3:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request3: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware4:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request4: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware5:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request5: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware6:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request6: {request.method} {request.path}")

        response = self.get_response(request)
        return response

class Middleware7:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger.info(f"Incoming Request7: {request.method} {request.path}")

        response = self.get_response(request)
        return response