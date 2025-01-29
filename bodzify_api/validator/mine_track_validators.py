
import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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
        raise ValidationError({
            'url': [_('There was an issue requesting the URL %(url)s') % {'url': url}]
        }, code=ValidationResponseCode.FIELD_URL_REQUEST_FAILED.value)


def validate_url(value: str):
    if not value.startswith('http'):
        raise ValidationError({
            'url': [_('%(url)s is not a valid URL') % {'url': value}]
        }, code=ValidationResponseCode.FIELD_INVALID_URL.value)
    if (not value.lower().endswith('.mp3')
        and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        raise ValidationError({
            'url': [_('%(url)s is not a valid audio file') % {'url': value}]
        }, code=ValidationResponseCode.FIELD_INVALID_FILE_TYPE.value)
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        raise ValidationError({
            'url': [_('%(url)s does not exist') % {'url': value}]
        }, code=ValidationResponseCode.FIELD_URL_NOT_FOUND.value)
