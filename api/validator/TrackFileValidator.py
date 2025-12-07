from pathlib import Path

import audiometa
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.post.Fields import Fields
from api.utils.file_path_utils import get_file_path


@deconstructible
class TrackFileValidator:

    AUDIO_MAGIC_BYTES = {
        b'ID3': 'audio/mpeg',
        b'\x4F\x67\x67\x53': 'audio/ogg',
        b'RIFF': 'audio/wav',
        b'.flac': 'audio/flac',
    }

    def __init__(self, field_name=None):
        self.field_name = field_name or Fields.TRACK_FILE_PUBLIC

    def __call__(self, value, field=None):
        self._validate_extension(value, field)
        self._validate_file_size(value, field)
        self._validate_content_type_is_audio_from_magic_bytes_and_content(value, field)

    def _validate_extension(self, value, field=None):
        allowed_extensions = [ext.lower() for ext in settings.UPLOADED_TRACK_FILE_EXTENSIONS]
        extension = Path(value.name).suffix[0:].lower()

        if extension not in allowed_extensions:
            message = _(
                "File extension '%(extension)s' is not allowed. "
                "Allowed extensions are: %(allowed_extensions)s."
            ) % {
                'extension': extension,
                'allowed_extensions': ', '.join(allowed_extensions),
            }

            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID, message)
            else:
                from api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID,
                    field_name=self.field_name)

    def _validate_file_size(self, file, field=None):
        track_size_max_in_ko = settings.UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
        if file.size > track_size_max_in_ko:
            message = _('File too large. Size should not exceed %(size).3f Mo.') % {
                'size': settings.UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO
            }
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.FILE_TOO_LARGE, message)
            else:
                from api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    field_name=self.field_name,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.FILE_TOO_LARGE
                )

        track_size_min = settings.UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO * 1000000
        if file.size < track_size_min:
            message = _('File too small. Size should be at least %(size).3f Mo.') % {
                'size': settings.UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO
            }
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.FILE_TOO_SMALL, message)
            else:
                from api.n.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    field_name=Fields.TRACK_FILE_PUBLIC,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.FILE_TOO_SMALL
                )

    def _validate_content_type_is_audio_from_magic_bytes_and_content(self, file, field=None):
        original_position = file.tell()
        first_few_bytes = file.read(4)
        file.seek(original_position)  # Reset file pointer to original position

        for magic_bytes, _ in self.AUDIO_MAGIC_BYTES.items():
            if first_few_bytes.startswith(magic_bytes):
                return

        is_valid_audio = False
        try:
            file_path = get_file_path(file)
            audiometa.get_unified_metadata(file=file_path)
            is_valid_audio = True
        except Exception:
            pass

        if not is_valid_audio:
            message = 'Invalid file format. Only audio files are allowed.'
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.TRACK_FILE_TYPE_INVALID, message)
            else:
                from api.exception.validation.app.AppValidationException import AppValidationException
                raise AppValidationException(
                    field_name=self.field_name, message=message,
                    field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_TYPE_INVALID)
