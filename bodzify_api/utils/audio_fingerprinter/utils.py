

import base64
import re

import requests

from bodzify_api import settings
from . import exception


class PostFields:
    FILENAME = 'filename'
    TITLE = 'title'
    USER_ID = 'userId'


class ResponseFields:
    class Ok:
        FINGERPRINT = 'fingerprint'
        DURATION = 'duration'

    class Exception:
        STATUS = 'status'
        MESSAGE = 'message'


SERVICE_EXCEPTION_CODE_PREFIXE = 'Audio Fingerprinter Exception Code '


def _get_service_exception_code_from_message(message):
    start_index = message.find(SERVICE_EXCEPTION_CODE_PREFIXE)
    if start_index != -1:
        substring_after_prefix = message[start_index + len(SERVICE_EXCEPTION_CODE_PREFIXE):]

        match = re.search(r'\d+', substring_after_prefix)
        if match:
            return int(match.group(0))
    return None


def post_fingerprint_audio(filename: str, title: str, user_id: str) -> tuple[bytes, float]:
    try:
        json_data = {
            PostFields.FILENAME: filename,
            PostFields.TITLE: title,
            PostFields.USER_ID: user_id
        }
        response = requests.post(settings.AFP_POST_FULL_URL,
                                 json=json_data,
                                 headers={'Content-Type': 'application/json'})
        response_json = response.json()
        if response.status_code == 200:
            fingerprint_bytes = base64.b64decode(
                response_json[ResponseFields.Ok.FINGERPRINT])
            duration = response_json[ResponseFields.Ok.DURATION]
            return fingerprint_bytes, duration
        elif response.status_code == 400:
            exception_code = _get_service_exception_code_from_message(
                response_json[ResponseFields.Exception.MESSAGE])
            if exception_code == 2:
                raise exception.WrongFileExtension(
                    response_json[ResponseFields.Exception.MESSAGE])
            elif exception_code == 3:
                raise exception.WrongFileType(response_json[ResponseFields.Exception.MESSAGE])
            elif exception_code == 4:
                raise exception.FileNotInPool(response_json[ResponseFields.Exception.MESSAGE])
            else:
                raise exception.BadRequestException(response_json)
        elif response.status_code == 500:
            raise exception.InternalServerException(response_json)
        elif response.status_code == 504:
            raise TimeoutError()
        elif response.status_code == 422:
            exception_code = _get_service_exception_code_from_message(
                response_json[ResponseFields.Exception.MESSAGE])
            if exception_code == 1:
                raise exception.FpcalcStatusException(response_json)
            else:
                raise exception.UnprocessableEntityException(response_json)
        elif response.status_code == 404:
            raise exception.ServiceNotFoundException()
        else:
            raise exception.AudioFingerprinterException(response_json)
    except requests.exceptions.ConnectionError as e:
        if str(e).find('Errno 61') != -1:
            raise exception.ServiceNotFoundException()
        else:
            raise ConnectionError(str(e))
