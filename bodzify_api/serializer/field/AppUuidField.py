from typing import Any, Optional, NoReturn
from uuid import UUID

from rest_framework import serializers

from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class AppUuidField(AppField, serializers.UUIDField):
    """
    Base field for UUID validation.
    Ensures that the input value is a valid UUID format.
    """

    default_error_messages = {
        'required': 'This field is required.',
        'invalid': 'Invalid UUID format.',
        'incorrect_type': 'Invalid UUID format.',
    }

    def __init__(self, **kwargs: Any) -> None:
        self.error_messages = {**self.default_error_messages}
        super().__init__(**kwargs)

    def fail(self, key: str, **kwargs: Any) -> NoReturn:
        """
        Raise an AppValidationError with appropriate error code and message.

        Args:
            key: The error key that maps to an error message
            **kwargs: Format parameters for the error message
        """
        try:
            msg = self.error_messages[key]
            if kwargs:
                msg = msg.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            msg = f"Invalid input for {class_name}."

        if key == 'required':
            code = FieldValidationErrorCode.REQUIRED
        elif key == 'incorrect_type':
            code = FieldValidationErrorCode.INVALID_FORMAT
        else:
            code = FieldValidationErrorCode.DEFAULT

        raise AppValidationError(
            field=self.get_error_field_name(),
            message=msg,
            field_validation_error_code=code
        )

    def to_internal_value(self, data: Any) -> UUID:
        return serializers.UUIDField.to_internal_value(self, data)

    def to_representation(self, value: Any) -> Optional[str]:
        """
        Returns the string representation of the UUID.
        """
        if value is None:
            return None
        return str(value)
