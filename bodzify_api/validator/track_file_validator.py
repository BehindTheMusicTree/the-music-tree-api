#!/usr/bin/env python

import os

from rest_framework.exceptions import ValidationError
from mutagen import File

from bodzify_api import settings


def validate_size(file):
    from bodzify_api.model.track.LibraryTrack import AttributesLabels
    track_size_max_in_ko = settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
    if file.size > track_size_max_in_ko:
        track_size_error_too_small_message = 'File too large. Size should not exceed {size:.3f} Mo.'
        raise ValidationError(
            {
                AttributesLabels.TRACK_FILE:
                track_size_error_too_small_message.format(size=settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO)
            })

    track_size_min = settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
    if file.size < track_size_min:
        track_size_error_too_small_message = 'File too small. Size should be at least {size:.3f} Mo.'
        raise ValidationError(
            {
                AttributesLabels.TRACK_FILE:
                track_size_error_too_small_message.format(size=settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO)
            })


def validate_content_type_is_audio(file):
    from bodzify_api.model.track.LibraryTrack import AttributesLabels

    AUDIO_MAGIC_BYTES = {b'ID3': 'audio/mpeg',
                         b'\x4F\x67\x67\x53': 'audio/ogg',
                         b'RIFF': 'audio/wav',
                         b'fLaC': 'audio/flac', }
    first_few_bytes = file.read(4)

    for magic_bytes, _ in AUDIO_MAGIC_BYTES.items():
        if first_few_bytes.startswith(magic_bytes):
            return

    audio = None
    try:
        audio = File(file)
    except Exception:
        pass

    error = audio is None
    if error:
        raise ValidationError({AttributesLabels.TRACK_FILE: 'Invalid file format. Only audio files are allowed.'})


def validate_filename_length(value):
    from bodzify_api.model.track.LibraryTrack import AttributesLabels
    try:
        filename = os.path.basename(value.file.name)
    except AttributeError:
        filename = os.path.basename(value.name)

    if len(filename) > settings.LIB_TRACK_FILENAME_LEN_MAX:
        raise ValidationError(
            {
                AttributesLabels.TRACK_FILE:
                f"Ensure this filename has at most {settings.LIB_TRACK_FILENAME_LEN_MAX} characters" +
                f"it has {len(filename)})."
            })
