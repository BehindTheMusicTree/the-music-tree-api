
import os
from pathlib import Path
from django.utils.translation import gettext as _
from mutagen import File  # type: ignore
from django.utils.deconstruct import deconstructible

from bodzify_api import settings
from .AppValidationError import AppValidationError
from .FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields


@deconstructible
class FileExtensionValidator:
    """
    Validator for checking if a file's extension is in the list of allowed extensions.
    Raises AppValidationError with the specified field name if validation fails.
    """

    def __init__(self, allowed_extensions=None, message=None, code=None, field_name=None):
        if allowed_extensions is not None:
            allowed_extensions = [
                allowed_extension.lower() for allowed_extension in allowed_extensions
            ]
        self.allowed_extensions = allowed_extensions
        self.message = message or _(
            "File extension '%(extension)s' is not allowed. "
            "Allowed extensions are: %(allowed_extensions)s."
        )
        self.code = code or FieldValidationErrorCode.INVALID_EXTENSION
        self.field_name = field_name

    def __call__(self, value, field=None):
        extension = Path(value.name).suffix[1:].lower()
        if (
            self.allowed_extensions is not None
            and extension not in self.allowed_extensions
        ):
            message = self.message % {
                'extension': extension,
                'allowed_extensions': ', '.join(self.allowed_extensions),
            }
            if field and hasattr(field, 'fail'):
                field.fail(self.code, message)
            else:
                raise AppValidationError(
                    message=message,
                    field_validation_error_code=self.code,
                    field_name=self.field_name
                )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.allowed_extensions == other.allowed_extensions
            and self.message == other.message
            and self.code == self.code
            and self.field_name == other.field_name
        )


@deconstructible
class FileSizeValidator:
    def __init__(self, field_name=None):
        self.field_name = field_name

    def __call__(self, file, field=None):
        track_size_max_in_ko = settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
        if file.size > track_size_max_in_ko:
            message = _('File too large. Size should not exceed %(size).3f Mo.') % {
                'size': settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO
            }
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.FILE_TOO_LARGE, message)
            else:
                raise AppValidationError(
                    field_name=self.field_name,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.FILE_TOO_LARGE
                )

        track_size_min = settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
        if file.size < track_size_min:
            message = _('File too small. Size should be at least %(size).3f Mo.') % {
                'size': settings.LIB_TRACK_FILE_SIZE_MIN_IN_MO
            }
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.FILE_TOO_SMALL, message)
            else:
                raise AppValidationError(
                    field_name=Fields.TRACK_FILE_PUBLIC,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.FILE_TOO_SMALL
                )


def validate_content_type_is_audio(file, field=None):

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
        if field and hasattr(field, 'fail'):
            field.fail(FieldValidationErrorCode.INVALID_FILE_TYPE, message)
        else:
            raise AppValidationError(
                field_name=Fields.TRACK_FILE_PUBLIC,
                message=message,
                field_validation_error_code=FieldValidationErrorCode.INVALID_FILE_TYPE
            )


def validate_filename_length(value, field=None):

    try:
        filename = os.path.basename(value.file.name)
    except AttributeError:
        filename = os.path.basename(value.name)

    if len(filename) > settings.LIB_TRACK_FILENAME_LEN_MAX:
        message = _('Ensure this filename has at most %(max_length)d characters (it has %(current_length)d).') % {
            'max_length': settings.LIB_TRACK_FILENAME_LEN_MAX,
            'current_length': len(filename)
        }
        if field and hasattr(field, 'fail'):
            field.fail(FieldValidationErrorCode.INVALID_FILENAME, message)
        else:
            raise AppValidationError(
                field_name=Fields.TRACK_FILE_PUBLIC,
                message=message,
                field_validation_error_code=FieldValidationErrorCode.INVALID_FILENAME
            )
