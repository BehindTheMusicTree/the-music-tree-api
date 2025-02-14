
import requests
from django.utils.translation import gettext as _

from .AppValidationError import AppValidationError
from .FieldValidationErrorCode import FieldValidationErrorCode


def check_if_url_contains_two_strings(url, string1, string2):
    return string1 in url and string2 in url


def check_if_remote_file_exists_using_get_request_with_range_header(url):
    try:
        response = requests.get(url, headers={'Range': 'bytes=0-10'}, allow_redirects=True)
        if response.status_code == 206:
            return True
        else:
            return False
    except Exception as e:
        # Since this is field validation, use from_field
        raise AppValidationError.from_field(
            field='url',
            message=_('There was an issue requesting the URL %(url)s') % {'url': url},
            code=FieldValidationErrorCode.URL_REQUEST_FAILED
        )


def validate_url(value: str):
    if not value.startswith('http'):
        # Since this is field validation, use from_field
        raise AppValidationError.from_field(
            field='url',
            message=_('%(url)s is not a valid URL') % {'url': value},
            code=FieldValidationErrorCode.INVALID_URL
        )
    if (not value.lower().endswith('.mp3')
        and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        # Since this is field validation, use from_field
        raise AppValidationError.from_field(
            field='url',
            message=_('%(url)s is not a valid audio file') % {'url': value},
            code=FieldValidationErrorCode.INVALID_FILE_TYPE
        )
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        # Since this is field validation, use from_field
        raise AppValidationError.from_field(
            field='url',
            message=_('%(url)s does not exist') % {'url': value},
            code=FieldValidationErrorCode.URL_NOT_FOUND
        )
