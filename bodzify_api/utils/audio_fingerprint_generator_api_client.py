#!/usr/bin/env python


import base64
from typing import Optional
import requests

from bodzify_api.settings import settings


class AudioFingerprintGeneratorError(Exception):
    pass


class BadRequestError(AudioFingerprintGeneratorError):
    pass


class InternalServerError(AudioFingerprintGeneratorError):
    pass


class TimeoutError(AudioFingerprintGeneratorError):
    pass


class UnprocessableEntityError(AudioFingerprintGeneratorError):
    pass


class NotFoundError(AudioFingerprintGeneratorError):
    pass


class ConnectionError(AudioFingerprintGeneratorError):
    pass


class POST_FIELDS:
    FILEPATH = 'filepath'


class RESPONSE_FIELDS:
    class OK:
        FINGERPRINT = 'fingerprint'
        DURATION = 'duration'


class AudioFingerprintGeneratorApiClient:

    @staticmethod
    def post_generate_audio_fingerprint(file_path: str) -> tuple[bytes, float]:
        try:
            response = requests.post(settings.AUDIO_FINGERPRINT_GENERATOR_POST_FULL_URL,
                                     json={POST_FIELDS.FILEPATH: file_path},
                                     headers={'Content-Type': 'application/json'})
            response_json = response.json()
            if response.status_code == 200:
                fingerprint_bytes = base64.b64decode(response_json[RESPONSE_FIELDS.OK.FINGERPRINT])
                duration = response_json[RESPONSE_FIELDS.OK.DURATION]
                return fingerprint_bytes, duration
            elif response.status_code == 400:
                raise BadRequestError(response_json)
            elif response.status_code == 500:
                raise InternalServerError(response_json)
            elif response.status_code == 504:
                raise TimeoutError(response_json)
            elif response.status_code == 422:
                raise UnprocessableEntityError(response_json)
            elif response.status_code == 404:
                raise NotFoundError(response_json)
            else:
                raise AudioFingerprintGeneratorError(response_json)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e)
