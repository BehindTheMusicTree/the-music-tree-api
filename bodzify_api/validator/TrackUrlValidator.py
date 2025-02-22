import requests
from django.utils.translation import gettext as _
from django.utils.deconstruct import deconstructible

from .AppValidationError import AppValidationError
from .FieldValidationErrorCode import FieldValidationErrorCode


@deconstructible
class TrackUrlValidator:
    """
    A validator that encapsulates all track URL validations:
    - URL format validation
    - Audio file extension validation
    - Remote file existence validation
    """

    ALLOWED_AUDIO_EXTENSIONS = ('.mp3', '.wav', '.flac')

    def __init__(self, field_name='url'):
        self.field_name = field_name

    def __call__(self, value: str, field=None):
        # Validate URL format
        self._validate_url_format(value, field)
        
        # Validate audio file extension
        self._validate_audio_extension(value, field)
        
        # Validate file existence
        self._validate_remote_file_exists(value, field)

    def _validate_url_format(self, value: str, field=None):
        if not value.startswith('http'):
            message = _('%(url)s is not a valid URL') % {'url': value}
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.INVALID_URL, message)
            else:
                raise AppValidationError(
                    field_name=self.field_name,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.INVALID_URL
                )

    def _validate_audio_extension(self, value: str, field=None):
        if not any(value.lower().endswith(ext) for ext in self.ALLOWED_AUDIO_EXTENSIONS):
            message = _('%(url)s is not a valid audio file') % {'url': value}
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.INVALID_FILE_TYPE, message)
            else:
                raise AppValidationError(
                    field_name=self.field_name,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.INVALID_FILE_TYPE
                )

    def _validate_remote_file_exists(self, value: str, field=None):
        try:
            response = requests.get(value, headers={'Range': 'bytes=0-10'}, allow_redirects=True)
            if response.status_code != 206:
                message = _('%(url)s does not exist') % {'url': value}
                if field and hasattr(field, 'fail'):
                    field.fail(FieldValidationErrorCode.URL_NOT_FOUND, message)
                else:
                    raise AppValidationError(
                        field_name=self.field_name,
                        message=message,
                        field_validation_error_code=FieldValidationErrorCode.URL_NOT_FOUND
                    )
        except Exception as e:
            message = _('There was an issue requesting the URL %(url)s') % {'url': value}
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.URL_REQUEST_FAILED, message)
            else:
                raise AppValidationError(
                    field_name=self.field_name,
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.URL_REQUEST_FAILED
                )

    def _check_if_url_contains_two_strings(self, url: str, string1: str, string2: str) -> bool:
        """Utility method to check if URL contains two specific strings"""
        return string1 in url and string2 in url