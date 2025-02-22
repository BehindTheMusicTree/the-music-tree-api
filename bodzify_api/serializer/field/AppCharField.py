from typing import Any, Optional

from rest_framework import serializers

from .AppField import AppField


class AppCharField(AppField, serializers.CharField):
    """
    Custom CharField that raises AppValidationError instead of DRF's ValidationError.
    This ensures consistent error handling across the application.

    Unlike PrimaryKeyRelatedField which natively uses fail() for validation errors,
    Django REST Framework's CharField directly raises ValidationError in its validation
    methods. Therefore, we override to_internal_value() to intercept validation
    and use fail() instead, ensuring our custom error handling is triggered.

    This approach matches how DRF's PrimaryKeyRelatedField works, where fail() is
    called automatically for validation errors.
    """

    def to_internal_value(self, data: Any) -> Optional[str]:
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not isinstance(data, str):
            self.fail('invalid')

        if not data and not self.allow_blank:
            self.fail('blank')

        if self.max_length is not None and len(data) > self.max_length:
            self.fail('max_length', max_length=self.max_length, length=len(data))

        if self.min_length is not None and len(data) < self.min_length:
            self.fail('min_length', min_length=self.min_length, length=len(data))

        return data
