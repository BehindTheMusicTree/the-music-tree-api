from typing import Any

from rest_framework.fields import Field, ListField

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class AppField(Field):
    """
    Base field class for all app-specific serializer fields.

    This field extends Django REST Framework's Field to provide:
    - Consistent error handling using AppValidationException (for input validation)
    - Automatic error code mapping from DRF validation keys
    - Proper field name handling for list fields (with [] suffix)

    Note: AppField fields can be used in both input and output serializers.
    The validation error handling (AppValidationException) is only triggered
    during input validation (to_internal_value). For output serializers,
    fields are used for serialization (to_representation) only.

    Key Features:
    ------------
    1. **Error Handling**: All validation errors are raised as AppValidationException
       instead of DRF's ValidationError, ensuring consistent error responses.

    2. **Error Code Mapping**: Automatically maps common DRF validation keys to
       application-specific error codes via `validation_error_code_mapping`.

    3. **List Field Names**: Automatically appends [] suffix to field names for
       list fields in error responses (e.g., `artists_names[]`).

    4. **Customizable Error Codes**: Child classes can override
       `validation_error_code_mapping` to customize error code mappings.

    Error Code Mapping:
    -------------------
    The following DRF validation keys are automatically mapped:
    - 'required' → FieldValidationErrorCode.REQUIRED
    - 'null' → FieldValidationErrorCode.REQUIRED
    - 'blank' → FieldValidationErrorCode.BLANK
    - 'invalid' → FieldValidationErrorCode.FORMAT_INVALID
    - 'max_length' → FieldValidationErrorCode.STRING_TOO_LONG
    - 'min_length' → FieldValidationErrorCode.STRING_TOO_SHORT
    - 'invalid_choice' → FieldValidationErrorCode.ENUM_INVALID
    - And more (see validation_error_code_mapping)

    Usage:
    ------
    All custom field classes should inherit from AppField:

    ```python
    class AppCharField(AppField, serializers.CharField):
        def to_internal_value(self, data):
            if not isinstance(data, str):
                self.fail('invalid')  # Raises AppValidationException
            return data
    ```

    The `fail()` method automatically:
    - Looks up the error message from error_messages
    - Maps the error key to an appropriate error code
    - Raises AppValidationException with proper field name

    Note:
    -----
    The base `to_internal_value()` method returns None to prevent
    NotImplementedError when subclasses call super().to_internal_value().
    All subclasses must override this method with their own implementation.
    """

    # Default mapping of DRF validation keys to our custom error codes
    validation_error_code_mapping: dict[str, FieldValidationErrorCode] = {
        'required': FieldValidationErrorCode.REQUIRED,
        'null': FieldValidationErrorCode.REQUIRED,
        'blank': FieldValidationErrorCode.BLANK,
        'invalid': FieldValidationErrorCode.FORMAT_INVALID,
        'invalid_extension': FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID,
        'invalid_choice': FieldValidationErrorCode.ENUM_INVALID,
        'does_not_exist': FieldValidationErrorCode.REFERENCE_INVALID,
        'incorrect_type': FieldValidationErrorCode.FORMAT_INVALID,
        'max_length': FieldValidationErrorCode.STRING_TOO_LONG,
        'min_length': FieldValidationErrorCode.STRING_TOO_SHORT,
        'max_value': FieldValidationErrorCode.RATING_TOO_LARGE,
        'min_value': FieldValidationErrorCode.RATING_TOO_SMALL,
        'max_size': FieldValidationErrorCode.FILE_TOO_LARGE,
        'min_size': FieldValidationErrorCode.FILE_TOO_SMALL,
    }

    invalid_message_validation_error_code_mapping: dict[str, FieldValidationErrorCode] = {
        'Not a valid string.': FieldValidationErrorCode.FORMAT_INVALID,
        'Invalid UUID format.': FieldValidationErrorCode.FORMAT_INVALID,
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

        if key == 'invalid':
            if msg.startswith('Failed to download file:'):
                code = FieldValidationErrorCode.TRACK_FILE_DOWNLOAD_FAILED
            code = self.invalid_message_validation_error_code_mapping.get(msg, FieldValidationErrorCode.DEFAULT)
        else:
            code = self.validation_error_code_mapping.get(key, FieldValidationErrorCode.DEFAULT)

        raise AppValidationException(
            field_name=self.get_error_field_name(), message=msg, field_validation_error_code=code)

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
