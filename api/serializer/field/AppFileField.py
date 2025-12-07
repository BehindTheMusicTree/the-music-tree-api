from typing import Any

from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from api.serializer.field.AppField import AppField


class AppFileField(AppField, serializers.FileField):
    """
    Custom FileField that calls fail() instead of DRF's ValidationError.
    This ensures consistent error handling across the application.
    """

    def to_internal_value(self, data: Any) -> Any:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not isinstance(data, UploadedFile):
            self.fail('invalid')

        if not data and not self.allow_null:
            self.fail('blank')

        if self.max_length is not None and len(data.name) > self.max_length:
            self.fail('max_length', max_length=self.max_length, length=len(data.name))

        return data
