from uuid import UUID
from typing import Any, Optional

from rest_framework.fields import Field

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class AppUuidField(Field):
    """
    Base field for UUID validation.
    Ensures that the input value is a valid UUID format.
    """

    def to_internal_value(self, data: Any) -> Optional[str]:
        """
        Validates that the input value is a valid UUID.
        Returns the string representation of the UUID if valid.
        """
        if data in [None, ''] and self.allow_null:
            return None

        try:
            uuid_obj = UUID(str(data))
        except (ValueError, AttributeError):
            raise AppValidationError(
                field=self.field_name or 'uuid',
                message='Invalid UUID format',
                code=FieldValidationErrorCode.INVALID_FORMAT
            )

        return str(uuid_obj)

    def to_representation(self, value: Any) -> Optional[str]:
        """
        Returns the string representation of the UUID.
        """
        if value is None:
            return None
        return str(value)