#!/usr/bin/env python

import requests
from rest_framework.exceptions import ValidationError

from bodzify_api.model.track.MineTrack import AttributesLabel


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
        raise ValidationError(f"There was an issue requesting ${AttributesLabel.URL}")


def validate_url(value):
    if not value.startswith('http'):
        raise ValidationError({AttributesLabel.URL: f"{value} is not a valid url."})
    if (not value.lower().endswith('.mp3')
        and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        raise ValidationError({AttributesLabel.URL: f"{value} is not a valid audio file."})
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        raise ValidationError({AttributesLabel.URL: f"{value} does not exist."})
