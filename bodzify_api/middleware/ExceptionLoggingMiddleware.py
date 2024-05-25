import logging
import traceback


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger = logging.getLogger('exceptions')
        logger.error(type(exception))
        logger.error(exception)
        # logger.error(type(exception) + " - " + exception)
        if exception.__traceback__ is not None:
            logger.error('\n'.join(
                traceback.format_exception(
                    etype=type(exception),
                    value=exception, tb=exception.__traceback__)))  # type: ignore
            print('\n'.join(
                traceback.format_exception(
                    etype=type(exception),
                    value=exception, tb=exception.__traceback__)))  # type: ignore
        else:
            logger.error('No traceback available for this exception')
        return None
