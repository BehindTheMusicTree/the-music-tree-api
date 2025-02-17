from typing import Any, Optional, TypeVar, Generic
from uuid import UUID
import uuid

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db import models
from rest_framework.request import Request
from rest_framework.relations import RelatedField

from bodzify_api.serializer.field.AppUuidField import AppUuidField
from bodzify_api.serializer.field.foreign_key.ForeignKeyField import ForeignKeyField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

T = TypeVar('T', bound=models.Model)


class PrivateUuidField(ForeignKeyField, AppUuidField, Generic[T]):
    """
    Field for UUID-based foreign keys that require user ownership verification.
    Extends RelatedField for proper type handling while incorporating functionality
    from AppUuidField for UUID validation and ForeignKeyField for foreign key operations.

    Type Parameters:
        T: A Django model type that this field references

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
        1. Validates UUID format
        2. Validates existence and user ownership
        3. Returns the model instance from queryset
        """
        if data in [None, ''] and self.allow_null:
            return None

        # Validate UUID format
        uuid_str = super(AppUuidField, self).to_internal_value(data)

        # Get filtered queryset with user ownership check
        queryset = self.get_queryset()
        if queryset is None:
            raise ImproperlyConfigured("Queryset must be set for this field")

        try:
            # Try to get the instance from the filtered queryset
            return queryset.get(uuid=uuid_str)
        except ObjectDoesNotExist:
            raise AppValidationError(
                field=self.get_error_field_name(),
                message='Object with this ID does not exist or does not belong to the user',
                code=FieldValidationErrorCode.RESOURCE_NOT_OWNED
            )
