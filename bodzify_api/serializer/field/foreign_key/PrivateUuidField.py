from typing import Any, Optional
from uuid import UUID

from django.core.exceptions import ImproperlyConfigured
from rest_framework.request import Request

from bodzify_api.serializer.field.AppUuidField import AppUuidField
from bodzify_api.serializer.field.foreign_key.ForeignKeyField import ForeignKeyField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class PrivateUuidField(AppUuidField, ForeignKeyField):
    """
    Field for UUID-based foreign keys that require user ownership verification.
    Extends AppUuidField for UUID validation and ForeignKeyField for foreign key functionality.

    This field ensures that:
    1. The value is a valid UUID (via AppUuidField)
    2. The referenced object exists and belongs to the current user (via ForeignKeyField)

    For standard single-model foreign keys with user ownership:
        class PlaylistSerializer(serializers.ModelSerializer):
            track = PrivateUuidField(queryset=LibraryTrack.objects.all())
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error_messages['does_not_exist'] = (
            'Object with this ID does not exist or does not belong to the user'
        )

    def get_request_user(self) -> Any:
        """Gets the user from request context with validation"""
        request = self.context.get('request')
        if not isinstance(request, Request):
            raise ImproperlyConfigured("request must be a Request instance.")
        return request.user

    def get_queryset(self) -> Any:
        """
        Returns the queryset filtered by the current user.
        """
        user = self.get_request_user()
        self.additional_filters = {'user': user}
        return super().get_queryset()

    def to_internal_value(self, data: Any) -> Optional[Any]:
        """
        Validates the input value:
        1. Validates UUID format using AppUuidField
        2. Validates existence and user ownership using ForeignKeyField
        """
        # First validate UUID format using AppUuidField
        uuid_str = super(AppUuidField, self).to_internal_value(data)
        if uuid_str is None:
            return None

        try:
            return ForeignKeyField.to_internal_value(self, uuid_str)
        except AppValidationError as e:
            if e.original_code == FieldValidationErrorCode.INVALID_REFERENCE:
                raise AppValidationError(
                    field=self.field_name,
                    message='Object with this ID does not exist or does not belong to the user',
                    code=FieldValidationErrorCode.RESOURCE_NOT_OWNED
                )
