from typing import Any, Generic, TypeVar

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from rest_framework.request import Request

from bodzify_api.model.uuid.UuidModel import UuidModel
from bodzify_api.serializer.field.AppUuidField import AppUuidField
from bodzify_api.serializer.field.foreign_key.ForeignKeyField import ForeignKeyField


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

    def get_request_user(self) -> Any:
        request = self.context.get('request')
        if not isinstance(request, Request):
            raise ImproperlyConfigured("request must be a Request instance.")
        return request.user

    def get_queryset(self) -> Any:
        user = self.get_request_user()
        self.additional_filters = {'user': user}
        return super().get_queryset()

    def to_internal_value(self, data: Any) -> UuidModel | None:
        if data in [None, ''] and self.allow_null:
            return None

        uuid = AppUuidField.to_internal_value(self, data)
        if uuid is None:
            return None

        return ForeignKeyField.to_internal_value(self, uuid)
