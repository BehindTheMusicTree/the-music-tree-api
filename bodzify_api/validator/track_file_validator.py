
import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from mutagen import File  # type: ignore

from bodzify_api import settings
from bodzify_api.model.track.lib.Fields import Fields
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode


def validate_size(file):
    track_size_max_in_ko = settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
    if file.size > track_size_max_in_ko:
        message = _('File too large. Size should not exceed %(size).3f Mo.') % {
            'size': settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO
        }
        raise ValidationError({Fields.TRACK_FILE: [message]}, code=ValidationResponseCode.FIELD_FILE_TOO_LARGE.value)

    track_size_min = settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
    if file.size < track_size_min:
        message = _('File too small. Size should be at least %(size).3f Mo.') % {
            'size': settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO
        }
        raise ValidationError({Fields.TRACK_FILE: [message]}, code=ValidationResponseCode.FIELD_FILE_TOO_SMALL.value)


def validate_content_type_is_audio(file):

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
        message = 'Invalid file format. Only audio files are allowed.'
        raise ValidationError(
            {Fields.TRACK_FILE_PUBLIC: [message]},
            code=ValidationResponseCode.FIELD_INVALID_FILE_TYPE.value)


def validate_filename_length(value):

    try:
        filename = os.path.basename(value.file.name)
    except AttributeError:
        filename = os.path.basename(value.name)

    if len(filename) > settings.LIB_TRACK_FILENAME_LEN_MAX:
        message = _('Ensure this filename has at most %(max_length)d characters (it has %(current_length)d).') % {
            'max_length': settings.LIB_TRACK_FILENAME_LEN_MAX,
            'current_length': len(filename)
        }
        raise ValidationError(
            {Fields.TRACK_FILE_PUBLIC: [message]},
            code=ValidationResponseCode.FIELD_INVALID_FILENAME.value)
