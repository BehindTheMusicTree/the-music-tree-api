#!/usr/bin/env python

from django.core.exceptions import ValidationError
from mutagen import File

import bodzify_api.settings as settings


def validate_size(file):
    track_size_max = settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
    if file.size > track_size_max:
        trackSizeErrorTooLargeMessage = 'File too large. Size should not exceed {size:.3f} Mo.'
        raise ValidationError(
            trackSizeErrorTooLargeMessage.format(size=track_size_max))

    track_size_min = settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
    if file.size < track_size_min:
        trackSizeErrorTooSmallMessage = 'File too small. Size should be at least {size:.3f} Mo.'
        raise ValidationError(
            trackSizeErrorTooSmallMessage.format(size=track_size_min))


def is_audio(file_path):
    try:
        audio = File(file_path)
    except Exception as e:
        return False

    return audio is not None


def validate_content_type_is_audio(file):

    AUDIO_MAGIC_BYTES = {
        b'ID3': 'audio/mpeg',
        b'\x4F\x67\x67\x53': 'audio/ogg',
        b'RIFF': 'audio/wav',
        b'fLaC': 'audio/flac',
    }

    first_few_bytes = file.read(4)

    for magic_bytes, content_type in AUDIO_MAGIC_BYTES.items():
        if first_few_bytes.startswith(magic_bytes):
            return

    if is_audio(file):
        return

    raise ValidationError('Invalid file format. Only audio files are allowed.')
