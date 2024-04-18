#!/usr/bin/env python

import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_if_url_contains_two_strings(url, string1, string2):
    return string1 in url and string2 in url


def validate_url(value):
    if not value.startswith('http'):
        raise ValidationError(
            _('%(value)s is not a valid url'),
            params={'value': value},
        )
    if (not value.lower().endswith('.mp3')
            and not value.lower().endswith('.wav')
            and not value.lower().endswith('.flac')):
        raise ValidationError(
            _('%(value)s is not a valid audio file'),
            params={'value': value},
        )
    if not check_if_remote_file_exists_using_get_request_with_range_header(value):
        raise ValidationError(
            _('%(value)s does not exist'),
            params={'value': value},
        )


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
