
from uuid import UUID

from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.request import Request

from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode

from bodzify_api import settings
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class UserContentObjectUuidField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = settings.UUID_LEN
        kwargs['required'] = True
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            uuid_obj = UUID(data)
        except (ValueError, AttributeError):
            raise_validation_error(
                message='Invalid UUID format',
                code=ValidationResponseCode.FIELD_INVALID_FORMAT.value
            )

        request = self.context['request']
        if not isinstance(request, Request):  # For linting purposes
            raise ImproperlyConfigured("request must be a Request instance.")
        user = request.user

        if not Playlist.objects.filter(user=user, uuid=uuid_obj).exists() \
                and not LibraryTrack.objects.filter(user=user, uuid=uuid_obj).exists():
            raise_validation_error(
                message='Object with this ID does not exist or does not belong to the user',
                code=ValidationResponseCode.FIELD_RESOURCE_NOT_OWNED.value
            )

        return str(uuid_obj)

    def to_representation(self, value):
        return str(value)
