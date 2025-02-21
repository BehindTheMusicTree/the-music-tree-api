
from abc import abstractmethod


class MusicbrainzRecordingLookupException(Exception):
    @abstractmethod
    def get_error_message(self):
        pass


class ApiErrorMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)


class DNSResolutionErrorMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(f"DNS resolution error: {exception_message}")


class UnknownStatusMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, status_code: str):
        super().__init__(f"Unknown lookup status code: {status_code}")


class ErrorStatusMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)


class InvalidFingerprintMusicbrainzRecordingLookupException(
        ErrorStatusMusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)


class InternalErrorMusicbrainzRecordingLookupException(ErrorStatusMusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)


class UnknownErrorCodeMusicbrainzRecordingLookupException(ErrorStatusMusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)
