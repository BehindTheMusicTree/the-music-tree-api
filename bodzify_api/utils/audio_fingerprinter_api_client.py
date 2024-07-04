#!/usr/bin/env python


import base64
import re
from typing import Optional
import requests

from bodzify_api import settings


class AudioFingerprinterError(Exception):
    def __init__(self, message=""):
        super().__init__(message)


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


class POST_FIELDS:
    FILE_NAME = 'filename'


class RESPONSE_FIELDS:
    class OK:
        FINGERPRINT = 'fingerprint'
        DURATION = 'duration'


class AudioFingerprinterApiClient:

    SERVICE_ERROR_CODE_PREFIXE = 'Audio Fingerprinter Error Code '

    @staticmethod
    def _get_service_error_code_from_message(message):
        start_index = message.find(AudioFingerprinterApiClient.SERVICE_ERROR_CODE_PREFIXE)
        if start_index != -1:
            substring_after_prefix = message[start_index + len(AudioFingerprinterApiClient.SERVICE_ERROR_CODE_PREFIXE):]

            match = re.search(r'\d+', substring_after_prefix)
            if match:
                return int(match.group(0))
        return None

    @staticmethod
    def post_fingerprint_audio(filename: str) -> tuple[bytes, float]:
        try:
            response = requests.post(settings.AUDIO_FINGERPRINTER_POST_FULL_URL,
                                     json={POST_FIELDS.FILE_NAME: filename},
                                     headers={'Content-Type': 'application/json'})
            response_json = response.json()
            if response.status_code == 200:
                fingerprint_bytes = base64.b64decode(response_json[RESPONSE_FIELDS.OK.FINGERPRINT])
                duration = response_json[RESPONSE_FIELDS.OK.DURATION]
                return fingerprint_bytes, duration
            elif response.status_code == 400:
                error_code = AudioFingerprinterApiClient._get_service_error_code_from_message(response_json)
                if error_code == 2:
                    raise WrongFileExtension(response_json)
                elif error_code == 3:
                    raise WrongFileType(response_json)
                elif error_code == 4:
                    raise FileNotInPool(response_json)
                else:
                    raise BadRequestError(response_json)
            elif response.status_code == 500:
                raise InternalServerError(response_json)
            elif response.status_code == 504:
                raise TimeoutError()
            elif response.status_code == 422:
                error_code = AudioFingerprinterApiClient._get_service_error_code_from_message(response_json)
                if error_code == 1:
                    raise FpcalcStatusError(response_json)
                else:
                    raise UnprocessableEntityError(response_json)
            elif response.status_code == 404:
                raise ServiceNotFoundError()
            else:
                raise AudioFingerprinterError(response_json)
        except requests.exceptions.ConnectionError as e:
            if str(e).find('Errno 61') != -1:
                raise ServiceNotFoundError()
            else:
                raise ConnectionError(str(e))
