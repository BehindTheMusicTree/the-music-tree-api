
from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from uuid import UUID


class UserFilteredPlayContentObjectUUIDField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = settings.UUID_LEN
        kwargs['required'] = True
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            uuid_obj = UUID(data)
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format.")

        user = self.context['request'].user
        if not Playlist.objects.filter(user=user, uuid=uuid_obj).exists() \
                and not LibraryTrack.objects.filter(user=user, uuid=uuid_obj).exists():
            raise serializers.ValidationError("Object with this ID does not exist or does not belong to the user.")

        return str(uuid_obj)

    def to_representation(self, value):
        return str(value)
