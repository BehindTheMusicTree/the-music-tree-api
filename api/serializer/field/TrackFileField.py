import os
from typing import Any

from django.core.files.uploadedfile import UploadedFile

from api import settings
from api.exception.validation.app.AppValidationException import AppValidationException
from api.serializer.field.AppField import AppField
from api.serializer.field.AppFileField import AppFileField


class TrackFileField(AppField):
    """
    A field that handles file uploads for tracks.
    """

    def __init__(self, **kwargs):
        self._allow_null = kwargs.get('allow_null', True)
        super().__init__(**kwargs)

        self.file_field = AppFileField(allow_null=self._allow_null)

    def bind(self, field_name: str, parent: Any) -> None:
        """
        Called when the field is bound to a serializer.
        Propagate the field name to child fields for proper error reporting.
        """
        super().bind(field_name, parent)
        if self.file_field:
            self.file_field.bind(field_name, parent)

    def to_internal_value(self, data: Any) -> Any:
        if data in [None, '']:
            if not self._allow_null:
                self.fail('null')
            return None

        if isinstance(data, UploadedFile):
            validated_file = self.file_field.to_internal_value(data)

            try:
                # I don't know why to_internal_value does not call run_validators automatically
                self.file_field.run_validators(validated_file)
            except AppValidationException as e:
                raise AppValidationException(field_name=self.get_error_field_name(),
                                             message=e.message,
                                             field_validation_error_code=e.field_validation_error_code)

            # Rename file if too long
            if len(validated_file.name) > settings.UPLOADED_TRACK_FILENAME_LEN_MAX:
                validated_file.name = validated_file.name[-settings.UPLOADED_TRACK_FILENAME_LEN_MAX:]
            return validated_file

        self.fail('invalid', detail='Field must be a valid audio file.')

    def to_representation(self, value: Any) -> str:
        if value is None:
            return ''

        # For files, return the file URL or empty string if no URL
        return value.url if value and hasattr(value, 'url') else ''
