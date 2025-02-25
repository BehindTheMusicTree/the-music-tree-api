from typing import Any, Dict
from rest_framework.fields import Field, ListField

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationError import AppValidationException


class AppField(Field):
    """
    Base field class for all app-specific serializer fields.
    Provides consistent error handling and field name handling across the application.
    """

    # Default mapping of DRF validation keys to our custom error codes
    validation_error_code_mapping: Dict[str, FieldValidationErrorCode] = {
        'required': FieldValidationErrorCode.REQUIRED,
        'null': FieldValidationErrorCode.REQUIRED,
        'blank': FieldValidationErrorCode.BLANK,
        'invalid': FieldValidationErrorCode.INVALID_FORMAT,
        'invalid_choice': FieldValidationErrorCode.INVALID_ENUM,
        'does_not_exist': FieldValidationErrorCode.INVALID_REFERENCE,
        'incorrect_type': FieldValidationErrorCode.INVALID_FORMAT,
        'max_length': FieldValidationErrorCode.STRING_TOO_LONG,
        'min_length': FieldValidationErrorCode.STRING_TOO_SHORT,
        'max_value': FieldValidationErrorCode.RATING_TOO_LARGE,
        'min_value': FieldValidationErrorCode.RATING_TOO_SMALL,
        'max_size': FieldValidationErrorCode.FILE_TOO_LARGE,
        'min_size': FieldValidationErrorCode.FILE_TOO_SMALL,
    }

    def fail(self, key: str, **kwargs: Any) -> None:
        """
        Raise an AppValidationError with appropriate error code and message.
        Maps common DRF validation keys to our custom error codes.

        Args:
            key: The error key that maps to an error message
            **kwargs: Format parameters for the error message

        Child classes can override validation_error_code_mapping to customize the error code mapping.
        """
        try:
            msg = self.error_messages[key]
            if kwargs:
                msg = msg.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            msg = f"Invalid input for {class_name}."

        # Get the error code from the mapping, defaulting to DEFAULT if not found
        code = self.validation_error_code_mapping.get(key, FieldValidationErrorCode.DEFAULT)

        raise AppValidationException(
            field_name=self.get_error_field_name(),
            message=msg,
            field_validation_error_code=code
        )

    def get_error_field_name(self) -> str | None:
        if hasattr(self, 'field_name') and self.field_name:
            field_name = self.field_name
            if getattr(self, 'many', False) or isinstance(self, ListField):
                field_name += '[]'
            return field_name
        return None

    def to_internal_value(self, data: Any) -> Any:
        """
        To prevent suclasses' calls to super().to_internal_value() from raising NotImplementedError.
        """
        return None
