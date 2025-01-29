
import requests
from django.utils.translation import gettext as _

from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode


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
        raise_validation_error(
            message=_('There was an issue requesting the URL %(url)s') % {'url': url},
            code=ValidationResponseCode.FIELD_URL_REQUEST_FAILED.value,
            field='url'
        )


def validate_url(value: str):
    if not value.startswith('http'):
        raise_validation_error(
            message=_('%(url)s is not a valid URL') % {'url': value},
            code=ValidationResponseCode.FIELD_INVALID_URL.value,
            field='url'
        )
    if (not value.lower().endswith('.mp3')
        and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        raise_validation_error(
            message=_('%(url)s is not a valid audio file') % {'url': value},
            code=ValidationResponseCode.FIELD_INVALID_FILE_TYPE.value,
            field='url'
        )
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        raise_validation_error(
            message=_('%(url)s does not exist') % {'url': value},
            code=ValidationResponseCode.FIELD_URL_NOT_FOUND.value,
            field='url'
        )
