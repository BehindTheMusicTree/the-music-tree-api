from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.model.playlist.base.output.Fields import \
    Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class PlaylistMinimumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME]
