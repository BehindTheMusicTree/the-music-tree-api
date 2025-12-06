from typing import Any

from rest_framework import serializers

from .AppField import AppField


class AppBooleanField(AppField, serializers.BooleanField):
    """
    Custom BooleanField that calls fail() instead of DRF's ValidationError.
    This ensures consistent error handling across the application.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure error messages are properly set
        if 'invalid' not in self.error_messages:
            self.error_messages['invalid'] = 'Must be a valid boolean.'

    def run_validation(self, data: Any = ...) -> bool | None:
        """
        Override run_validation to ensure our to_internal_value is called.
        This bypasses DRF's BooleanField.run_validation which might call
        AppField.to_internal_value (which returns None) via super().
        """
        from rest_framework.fields import empty as empty_sentinel
        if data is ...:
            data = self.get_value({})
            if data is empty_sentinel:
                data = None
        # Call our to_internal_value directly
        return self.to_internal_value(data)

    def to_internal_value(self, data: Any) -> bool | None:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        # Handle boolean and string boolean representations
        if isinstance(data, bool):
            return data
        if isinstance(data, str):
            data_lower = data.lower().strip()
            if data_lower == 'true':
                return True
            if data_lower == 'false':
                return False

        # If we get here, the value is invalid
        self.fail('invalid')
        return None  # Never reached, just for type checking
