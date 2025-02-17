from uuid import UUID
from typing import Optional, Any

from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.request import Request

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api import settings


class BasePrivateUuidField(serializers.CharField):
    """
    Base field for handling UUID validation with user ownership verification.
    Provides common functionality for UUID fields that need to verify user ownership.
    """
    field_name: str = ''
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = settings.UUID_LEN
        kwargs['required'] = kwargs.get('required', True)
        super().__init__(*args, **kwargs)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        if field_name is None:
            raise ImproperlyConfigured("field_name cannot be None")
        self.field_name = str(field_name)

    def validate_uuid_format(self, data: str) -> UUID:
        """Validates UUID format and returns UUID object"""
        try:
            return UUID(data)
        except (ValueError, AttributeError):
            raise AppValidationError(
                field=self.field_name or 'uuid',
                message='Invalid UUID format',
                code=FieldValidationErrorCode.INVALID_FORMAT
            )

    def get_request_user(self) -> Any:
        """Gets the user from request context with validation"""
        request = self.context.get('request')
        if not isinstance(request, Request):
            raise ImproperlyConfigured("request must be a Request instance.")
        return request.user

    def verify_user_ownership(self, uuid_obj: UUID, user: Any) -> bool:
        """
        Template method for verifying user ownership of the UUID.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement verify_user_ownership")

    def to_internal_value(self, data: str) -> Optional[str]:
        if data in [None, ''] and getattr(self, 'allow_null', False):
            return None
            
        uuid_obj = self.validate_uuid_format(data)
        user = self.get_request_user()

        if not self.verify_user_ownership(uuid_obj, user):
            raise AppValidationError(
                field=self.field_name or 'uuid',
                message='Object with this ID does not exist or does not belong to the user',
                code=FieldValidationErrorCode.RESOURCE_NOT_OWNED
            )

        return str(uuid_obj)

    def to_representation(self, value: Any) -> str:
        return str(value)