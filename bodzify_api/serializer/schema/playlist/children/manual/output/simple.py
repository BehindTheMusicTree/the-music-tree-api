from rest_framework import serializers

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    LIB_TRACKS_COUNT = AvailableFields.LIB_TRACKS_COUNT


class ManualPlaylistSimpleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT]
