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
        requestLogger = logging.getLogger('request')
        requestDebugLogger = logging.getLogger('django.request')

        logMessage = f"Incoming Request: {request.method} {request.path} {request.META['REMOTE_ADDR']} "
        requestLogger.info(logMessage)
        requestDebugLogger.info(logMessage)
        requestDebugLogger.info(_generate_log_about_headers(request))

        response = self.get_response(request)
        responseCodeMessage = f"Response status code: {response.status_code}"
        requestLogger.info(responseCodeMessage)
        requestDebugLogger.info(responseCodeMessage)
        return response
