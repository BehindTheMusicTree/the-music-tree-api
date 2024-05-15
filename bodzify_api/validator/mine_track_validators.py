#!/usr/bin/env python

import requests
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bodzify_api.model.track.MineTrack import ATTRIBUTES_LABEL


def check_if_url_contains_two_strings(url, string1, string2):
    return string1 in url and string2 in url


def validate_url(value):
    if not value.startswith('http'):
        raise ValidationError({ATTRIBUTES_LABEL.URL: f"{value} is not a valid url."})
    if (not value.lower().endswith('.mp3')
        and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        raise ValidationError({ATTRIBUTES_LABEL.URL: f"{value} is not a valid audio file."})
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        raise ValidationError({ATTRIBUTES_LABEL.URL: f"{value} does not exist."})


def check_if_remote_file_exists_using_get_request_with_range_header(url):
    try:
        response = requests.get(
            url, headers={'Range': 'bytes=0-10'}, allow_redirects=True)
        if response.status_code == 206:
            return True
        else:
            return False
    except:
        return False
