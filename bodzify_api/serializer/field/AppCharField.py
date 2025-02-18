from typing import Any, Optional

from rest_framework import serializers

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class AppCharField(serializers.CharField):
    """
    Custom CharField that raises AppValidationError instead of DRF's ValidationError.
    This ensures consistent error handling across the application.
    """

    def run_validation(self, data: Any = serializers.empty) -> Any:
        if data == serializers.empty:
            if self.required:
                self.fail('required')
            return self.get_default()

        if data == '' or (self.trim_whitespace and str(data).strip() == ''):
            if self.allow_blank:
                return ''
            self.fail('blank')

        data = self.to_internal_value(data)
        self.run_validators(data)
        return data

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

        # Get field name, defaulting to empty string if not available
        field_name: Optional[str] = getattr(self, 'field_name', '')
        if field_name:
            raise AppValidationError(field=field_name, message=message, code=code)
        else:
            raise AppValidationError(message=message, code=code)
