from typing import Any

from rest_framework import serializers

from .AppField import AppField


class AppEmailField(AppField, serializers.EmailField):
    """
    Custom EmailField that calls fail() instead of DRF's ValidationError.
    This ensures consistent error handling across the application.
    """

    def to_internal_value(self, data: Any) -> str | None:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not isinstance(data, str):
            self.fail('invalid')

        if not data and not self.allow_blank:
            self.fail('blank')

        # Email validation
        if not self.run_validation(data):
            self.fail('invalid')

        return data

    def run_validation(self, data: Any = None) -> bool:
        try:
            return super().run_validation(data) is not None
        except serializers.ValidationError:
            return False