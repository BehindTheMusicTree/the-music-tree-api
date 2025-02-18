from typing import Any, Optional

from rest_framework import serializers

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
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

    def fail(self, key: str, **kwargs: Any) -> None:
        """
        Raise an AppValidationError with appropriate error code and message.

        Args:
            key: The error key that maps to an error message
            **kwargs: Format parameters for the error message
        """
        try:
            message = self.error_messages[key]
            if kwargs:
                message = message.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            message = f"Invalid input for {class_name}."

        if key == 'required':
            code = FieldValidationErrorCode.REQUIRED
        elif key == 'blank':
            code = FieldValidationErrorCode.BLANK
        elif key == 'max_length':
            code = FieldValidationErrorCode.STRING_TOO_LONG
        elif key == 'min_length':
            code = FieldValidationErrorCode.STRING_TOO_SHORT
        elif key == 'invalid':
            code = FieldValidationErrorCode.INVALID_FORMAT
        else:
            code = FieldValidationErrorCode.INVALID_FORMAT

        raise AppValidationError(field=self.get_error_field_name(), message=message, code=code)

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
