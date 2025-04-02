from typing import Any

from rest_framework.fields import DictField

from bodzify_api.serializer.field.AppField import AppField


class AppDictField(AppField, DictField):
    """
    Custom DictField that calls fail() instead of DRF's ValidationError.
    This ensures consistent error handling across the application.
    """

    def to_internal_value(self, data: Any) -> dict:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return {}

        if not isinstance(data, dict):
            self.fail('invalid')

        return data
