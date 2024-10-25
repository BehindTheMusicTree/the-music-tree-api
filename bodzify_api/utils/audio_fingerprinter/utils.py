#!/usr/bin/env python


import base64
import re

import requests

from bodzify_api import settings
from . import error


class PostFields:
    FILENAME = 'filename'
    TITLE = 'title'
    USER_ID = 'userId'


class ResponseFields:
    class Ok:
        FINGERPRINT = 'fingerprint'
        DURATION = 'duration'

    class Error:
        STATUS = 'status'
        MESSAGE = 'message'


SERVICE_ERROR_CODE_PREFIXE = 'Audio Fingerprinter Error Code '


def _get_service_error_code_from_message(message):
    start_index = message.find(SERVICE_ERROR_CODE_PREFIXE)
    if start_index != -1:
        substring_after_prefix = message[start_index + len(SERVICE_ERROR_CODE_PREFIXE):]

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
            error_code = _get_service_error_code_from_message(
                response_json[ResponseFields.Error.MESSAGE])
            if error_code == 2:
                raise error.WrongFileExtension(
                    response_json[ResponseFields.Error.MESSAGE])
            elif error_code == 3:
                raise error.WrongFileType(response_json[ResponseFields.Error.MESSAGE])
            elif error_code == 4:
                raise error.FileNotInPool(response_json[ResponseFields.Error.MESSAGE])
            else:
                raise error.BadRequestError(response_json)
        elif response.status_code == 500:
            raise error.InternalServerError(response_json)
        elif response.status_code == 504:
            raise TimeoutError()
        elif response.status_code == 422:
            error_code = _get_service_error_code_from_message(
                response_json[ResponseFields.Error.MESSAGE])
            if error_code == 1:
                raise error.FpcalcStatusError(response_json)
            else:
                raise error.UnprocessableEntityError(response_json)
        elif response.status_code == 404:
            raise error.ServiceNotFoundError()
        else:
            raise error.AudioFingerprinterError(response_json)
    except requests.exceptions.ConnectionError as e:
        if str(e).find('Errno 61') != -1:
            raise error.ServiceNotFoundError()
        else:
            raise ConnectionError(str(e))
