
from abc import abstractmethod


class MusicbrainzRecordingLookupException(Exception):
    @abstractmethod
    def get_error_message(self):
        pass


class ApiErrorMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)


class UnknownStatusCodeMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, status_code: str):
        super().__init__(f"Unknown lookup status code: {status_code}")


class UnknownErrorMusicbrainzRecordingLookupException(MusicbrainzRecordingLookupException):
    def __init__(self, exception_message: str):
        super().__init__(exception_message)
