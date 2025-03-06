from pathlib import Path

from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
from mutagen import File  # type: ignore

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields


@deconstructible
class TrackFileValidator:

    AUDIO_MAGIC_BYTES = {
        b'ID3': 'audio/mpeg',
        b'\x4F\x67\x67\x53': 'audio/ogg',
        b'RIFF': 'audio/wav',
        b'fLaC': 'audio/flac',
    }

    def __init__(self, field_name=None):
        self.field_name = field_name or Fields.TRACK_FILE_PUBLIC

    def __call__(self, value, field=None):
        self._validate_extension(value, field)
        self._validate_file_size(value, field)
        self._validate_content_type_is_audio_from_magic_bytes_and_content(value, field)

    def _validate_extension(self, value, field=None):
        allowed_extensions = [ext.lower() for ext in settings.LIB_TRACK_FILE_EXTENSIONS]
        extension = Path(value.name).suffix[1:].lower()

        if extension not in allowed_extensions:
            message = _(
                "File extension '%(extension)s' is not allowed. "
                "Allowed extensions are: %(allowed_extensions)s."
            ) % {
                'extension': extension,
                'allowed_extensions': ', '.join(allowed_extensions),
            }

            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.AUDIO_FILE_EXTENSION_INVALID, message)
            else:
                from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    message=message, field_validation_error_code=FieldValidationErrorCode.AUDIO_FILE_EXTENSION_INVALID,
                    field_name=self.field_name)

    def _validate_file_size(self, file, field=None):
        track_size_max_in_ko = settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
        if file.size > track_size_max_in_ko:
            message = _('File too large. Size should not exceed %(size).3f Mo.') % {
                'size': settings.LIB_TRACK_FILE_SIZE_MAX_IN_MO
            }
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.FILE_TOO_LARGE, message)
            else:
                from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
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
                from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    field_name=Fields.TRACK_FILE_PUBLIC,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.FILE_TOO_SMALL
                )

    def _validate_content_type_is_audio_from_magic_bytes_and_content(self, file, field=None):
        first_few_bytes = file.read(4)

        for magic_bytes, _ in self.AUDIO_MAGIC_BYTES.items():
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
                field.fail(FieldValidationErrorCode.AUDIO_FILE_TYPE_INVALID, message)
            else:
                from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    field_name=self.field_name, message=message,
                    field_validation_error_code=FieldValidationErrorCode.AUDIO_FILE_TYPE_INVALID)
