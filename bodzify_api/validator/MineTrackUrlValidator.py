#!/usr/bin/env python
import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bodzify_api import settings

def checkIfUrlContainsTwoStrings(url, string1, string2):
    return string1 in url and string2 in url

def validateUrl(value):
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
    if not checkIfRemoteFileExisteUsingGetRequestWithRangeHeader(value):
        raise ValidationError(
            _('%(value)s does not exist'),
            params={'value': value},
        )

def checkIfRemoteFileExisteUsingGetRequestWithRangeHeader(url):
    try:
        r = requests.get(url, headers={'Range': 'bytes=0-10'}, allow_redirects=True)
        if r.status_code == 206:
            return True
        else:
            return False
    except:
        return False