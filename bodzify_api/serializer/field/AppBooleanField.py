from typing import Any

from rest_framework import serializers

from .AppField import AppField


class AppBooleanField(AppField, serializers.BooleanField):
    """
    Custom BooleanField that calls fail() instead of DRF's ValidationError.
    This ensures consistent error handling across the application.
    """

    def to_internal_value(self, data: Any) -> bool | None:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        try:
            if data in (True, 'true', 't', 'True', '1', 1):
                return True
            if data in (False, 'false', 'f', 'False', '0', 0):
                return False
        except (TypeError, ValueError):
            pass

        self.fail('invalid')
        return None  # Never reached, just for type checking