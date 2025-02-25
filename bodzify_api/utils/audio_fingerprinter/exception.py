

class AudioFingerprinterException(Exception):
    def __init__(self, message=""):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class BadRequestException(AudioFingerprinterException):
    def __init__(self, message=""):
        super().__init__(message)


class WrongFileExtension(BadRequestException):
    def __init__(self, message=""):
        super().__init__(message)


class WrongFileType(BadRequestException):
    def __init__(self, message=""):
        super().__init__(message)


class FileNotInPool(BadRequestException):
    def __init__(self, message=""):
        super().__init__(message)


class UnknownBadRequestException(BadRequestException):
    def __init__(self, message=""):
        super().__init__("Unprocessable bad request error: " + message)


class InternalServerException(AudioFingerprinterException):
    def __init__(self, message=""):
        super().__init__(message)


class TimeoutException(AudioFingerprinterException):
    pass


class UnprocessableEntityException(AudioFingerprinterException):
    def __init__(self, message=""):
        super().__init__(message)


class FpcalcStatusException(UnprocessableEntityException):
    def __init__(self, message=""):
        super().__init__(message)


class UnknownUnprocessableEntityException(AudioFingerprinterException):
    def __init__(self, message=""):
        super().__init__("Unknown unprocessable entity error: " + message)


class ServiceNotFoundException(AudioFingerprinterException):
    pass


class ConnectionException(AudioFingerprinterException):
    pass
