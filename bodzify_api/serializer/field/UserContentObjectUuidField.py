
from uuid import UUID

from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.request import Request

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

from bodzify_api import settings
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class UserContentObjectUuidField(serializers.CharField):
    field_name: str

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = settings.UUID_LEN
        kwargs['required'] = True
        super().__init__(*args, **kwargs)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        if field_name is None:
            raise ImproperlyConfigured("field_name cannot be None")

    def to_internal_value(self, data):
        try:
            uuid_obj = UUID(data)
        except (ValueError, AttributeError):
            # Since this is field validation (to_internal_value), use from_field
            raise AppValidationError.from_field(
                field=self.field_name,
                message='Invalid UUID format',
                code=FieldValidationErrorCode.INVALID_FORMAT
            )

        request = self.context['request']
        if not isinstance(request, Request):  # For linting purposes
            raise ImproperlyConfigured("request must be a Request instance.")
        user = request.user

        if not Playlist.objects.filter(user=user, uuid=uuid_obj).exists() \
                and not LibraryTrack.objects.filter(user=user, uuid=uuid_obj).exists():
            # Since this is field validation (to_internal_value), use from_field
            raise AppValidationError.from_field(
                field=self.field_name,
                message='Object with this ID does not exist or does not belong to the user',
                code=FieldValidationErrorCode.RESOURCE_NOT_OWNED
            )

        return str(uuid_obj)

    def to_representation(self, value):
        return str(value)
