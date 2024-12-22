
from uuid import UUID

from rest_framework import serializers
from rest_framework.request import Request

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
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format.")

        request = self.context['request']
        if not isinstance(request, Request):  # For linting purposes
            raise ValueError("request must be an Request instance.")
        user = request.user

        if not Playlist.objects.filter(user=user, uuid=uuid_obj).exists() \
                and not LibraryTrack.objects.filter(user=user, uuid=uuid_obj).exists():
            raise serializers.ValidationError("Object with this ID does not exist or does not belong to the user.")

        return str(uuid_obj)

    def to_representation(self, value):
        return str(value)
