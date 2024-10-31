
import requests
from rest_framework.exceptions import ValidationError


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
        raise ValidationError(f"There was an issue requesting the url {url}")


def validate_url(value: str):
    if not value.startswith('http'):
        raise ValidationError(f"url: {value} is not a valid url.")
    if (not value.lower().endswith('.mp3')
        and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        raise ValidationError(f"url: {value} is not a valid audio file.")
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        raise ValidationError(f"url: {value} does not exist.")
