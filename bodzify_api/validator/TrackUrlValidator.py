import requests
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


@deconstructible
class TrackUrlValidator(BaseValidator):
    """
    A validator that encapsulates all track URL validations:
    - URL format validation
    - Audio file extension validation
    - Remote file existence validation
    """

    ALLOWED_AUDIO_EXTENSIONS = ('.mp3', '.wav', '.flac')

    def __init__(self, field_name='url', message=None):
        super().__init__(None, message)  # We don't use limit_value
        self.field_name = field_name

    def __call__(self, value):
        if not isinstance(value, str):
            raise ValidationError(_('%(url)s is not a valid URL') % {'url': value})

        # Validate URL format
        self._validate_url_format(value)

        # Validate audio file extension
        self._validate_audio_extension(value)

        # Validate file existence
        self._validate_remote_file_exists(value)

    def _validate_url_format(self, value: str):
        if not value.startswith('http'):
            raise ValidationError(
                _('%(url)s is not a valid URL') % {'url': value},
                code=str(FieldValidationErrorCode.INVALID_URL),
                params={'value': value}
            )

    def _validate_audio_extension(self, value: str):
        if not any(value.lower().endswith(ext) for ext in self.ALLOWED_AUDIO_EXTENSIONS):
            raise ValidationError(
                _('%(url)s is not a valid audio file') % {'url': value},
                code=str(FieldValidationErrorCode.INVALID_FILE_TYPE),
                params={'value': value}
            )

    def _validate_remote_file_exists(self, value: str):
        try:
            response = requests.get(value, headers={'Range': 'bytes=0-10'}, allow_redirects=True)
            if response.status_code != 206:
                raise ValidationError(
                    _('%(url)s does not exist') % {'url': value},
                    code=str(FieldValidationErrorCode.URL_NOT_FOUND),
                    params={'value': value}
                )
        except Exception as e:
            raise ValidationError(
                _('There was an issue requesting the URL %(url)s') % {'url': value},
                code=str(FieldValidationErrorCode.URL_REQUEST_FAILED),
                params={'value': value}
            )

    def _check_if_url_contains_two_strings(self, url: str, string1: str, string2: str) -> bool:
        """Utility method to check if URL contains two specific strings"""
        return string1 in url and string2 in url
