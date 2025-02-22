from typing import Any, Optional, NoReturn
from uuid import UUID

from rest_framework import serializers

from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class AppUuidField(AppField, serializers.UUIDField):

    default_error_messages = {
        'required': 'This field is required.',
        'invalid': 'Invalid UUID format.',
        'incorrect_type': 'Invalid UUID format.',
    }

    def __init__(self, **kwargs: Any) -> None:
        self.error_messages = {**self.default_error_messages}
        super().__init__(**kwargs)

    def to_internal_value(self, data: Any) -> Optional[UUID]:
        """
        Validate that the input is a valid UUID.
        Unlike UUIDField which directly raises ValidationError, we use fail()
        to ensure consistent error handling across the application.
        """
        if data is None:
            if not self.allow_null:
                self.fail('null')
            return None

        if not isinstance(data, (str, UUID)):
            self.fail('incorrect_type')

        try:
            if isinstance(data, str):
                return UUID(data)
            return data
        except (ValueError, AttributeError):
            self.fail('invalid')

    def to_representation(self, value: Any) -> Optional[str]:
        return serializers.UUIDField.to_representation(self, value)
