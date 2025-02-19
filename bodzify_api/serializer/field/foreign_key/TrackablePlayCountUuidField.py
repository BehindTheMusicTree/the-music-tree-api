from typing import Union, Type, Optional
from uuid import UUID

from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Model
from rest_framework.request import Request

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TrackablePlayCountUuidField(PrivateUuidField):
    """
    A field that validates a UUID refers to a trackable play count object (Playlist or LibraryTrack)
    owned by the current user.
    """

    def __init__(self, **kwargs):
        # Initialize with a dummy queryset, we'll handle the actual validation in to_internal_value
        super().__init__(queryset=Playlist.objects.none(), **kwargs)

    def _get_object_by_uuid(
            self, uuid_value: UUID, user: Union[User, AnonymousUser],
            model_class: Type[Model]) -> Optional[Model]:
        """Helper method to get an object by UUID and user."""
        if isinstance(user, AnonymousUser):
            return None

        try:
            return model_class.objects.get(uuid=uuid_value, user=user)
        except model_class.DoesNotExist:
            return None

    def to_internal_value(self, data):
        if data in [None, ''] and self.allow_null:
            return None

        uuid_value = super(PrivateUuidField, self).to_internal_value(data)
        request = self.context.get('request')

        if not isinstance(request, Request):
            raise ValueError("TrackablePlayCountUuidField requires request in the context")

        user = request.user

        content_object = (
            self._get_object_by_uuid(uuid_value, user, Playlist) or
            self._get_object_by_uuid(uuid_value, user, LibraryTrack)
        )

        if not content_object:
            raise AppValidationError(
                field=self.field_name or 'trackable_play_count_uuid',
                message='Invalid content object UUID',
                field_validation_error_code=FieldValidationErrorCode.RESOURCE_NOT_OWNED
            )

        return uuid_value
