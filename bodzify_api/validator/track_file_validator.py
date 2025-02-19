
import os

from django.utils.translation import gettext as _
from mutagen import File  # type: ignore

from bodzify_api import settings
from bodzify_api.model.track.lib.Fields import Fields
from .AppValidationError import AppValidationError
from .FieldValidationErrorCode import FieldValidationErrorCode


def validate_size(file):
    track_size_max_in_ko = settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
    if file.size > track_size_max_in_ko:
        message = _('File too large. Size should not exceed %(size).3f Mo.') % {
            'size': settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO
        }
        raise AppValidationError(
            field_name=Fields.TRACK_FILE,
            message=message,
            field_validation_error_code=FieldValidationErrorCode.FILE_TOO_LARGE
        )

    track_size_min = settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
    if file.size < track_size_min:
        message = _('File too small. Size should be at least %(size).3f Mo.') % {
            'size': settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO
        }
        raise AppValidationError(
            field_name=Fields.TRACK_FILE,
            message=message,
            field_validation_error_code=FieldValidationErrorCode.FILE_TOO_SMALL
        )


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
        raise AppValidationError(
            field_name=Fields.TRACK_FILE_PUBLIC,
            message=message,
            field_validation_error_code=FieldValidationErrorCode.INVALID_FILE_TYPE
        )


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
        raise AppValidationError(
            field_name=Fields.TRACK_FILE_PUBLIC,
            message=message,
            field_validation_error_code=FieldValidationErrorCode.INVALID_FILENAME
        )
