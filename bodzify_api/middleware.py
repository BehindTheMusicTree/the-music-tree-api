#!/usr/bin/env python

import logging


def _generate_log_about_headers(request):
    logMessage = "Headers: "
    for header in request.headers:
        logMessage += f"{header}: {request.headers[header]} "
    return logMessage


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logMessage = f"Incoming Request: {request.method} {request.path} {request.META['REMOTE_ADDR']} "
        requestLogger = logging.getLogger('request')
        requestLogger.info(logMessage)
        requestDebugLogger = logging.getLogger('django.request')
        requestDebugLogger.info(logMessage)
        requestDebugLogger.info(_generate_log_about_headers(request))

        response = self.get_response(request)
        requestLogger.info('Response status code: %s', response.status_code)
        return response
