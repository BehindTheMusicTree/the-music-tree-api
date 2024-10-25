#!/usr/bin/env python


class AudioFingerprinterError(Exception):
    def __init__(self, message=""):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class BadRequestError(AudioFingerprinterError):
    def __init__(self, message=""):
        super().__init__(message)


class WrongFileExtension(BadRequestError):
    def __init__(self, message=""):
        super().__init__(message)


class WrongFileType(BadRequestError):
    def __init__(self, message=""):
        super().__init__(message)


class FileNotInPool(BadRequestError):
    def __init__(self, message=""):
        super().__init__(message)


class UnknownBadRequestError(BadRequestError):
    def __init__(self, message=""):
        super().__init__("Unprocessable bad request error: " + message)


class InternalServerError(AudioFingerprinterError):
    def __init__(self, message=""):
        super().__init__(message)


class TimeoutError(AudioFingerprinterError):
    pass


class UnprocessableEntityError(AudioFingerprinterError):
    def __init__(self, message=""):
        super().__init__(message)


class FpcalcStatusError(UnprocessableEntityError):
    def __init__(self, message=""):
        super().__init__(message)


class UnknownUnprocessableEntityError(AudioFingerprinterError):
    def __init__(self, message=""):
        super().__init__("Unknown unprocessable entity error: " + message)


class ServiceNotFoundError(AudioFingerprinterError):
    pass


class ConnectionError(AudioFingerprinterError):
    pass
