"""Custom file extension validator that uses our validation error classes."""

from pathlib import Path
from typing import Optional, List

from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .FieldValidationErrorCode import FieldValidationErrorCode


@deconstructible
class FileExtensionValidator:
    """
    Validator for checking if a file's extension is in the list of allowed extensions.
    This is our custom version that uses our own validation error classes.
    """

    message = _(
        "File extension '%(extension)s' is not allowed. "
        "Allowed extensions are: %(allowed_extensions)s."
    )

    def __init__(
        self,
        allowed_extensions: Optional[List[str]] = None,
        message: Optional[str] = None,
        field_name: Optional[str] = None
    ):
        if allowed_extensions is not None:
            allowed_extensions = [ext.lower() for ext in allowed_extensions]
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message
        self.field_name = field_name

    def __call__(self, value, field=None):
        extension = Path(value.name).suffix[1:].lower()
        if (
            self.allowed_extensions is not None
            and extension not in self.allowed_extensions
        ):
            message = self.message % {
                'extension': extension,
                'allowed_extensions': ', '.join(self.allowed_extensions),
            }
            if field and hasattr(field, 'fail'):
                field.fail(FieldValidationErrorCode.INVALID_FILE_TYPE, message)
            else:
                from .AppValidationError import AppValidationError
                raise AppValidationError(
                    message=message,
                    field_validation_error_code=FieldValidationErrorCode.INVALID_FILE_TYPE,
                    field_name=self.field_name
                )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.allowed_extensions == other.allowed_extensions
            and self.message == other.message
            and self.field_name == other.field_name
        )
