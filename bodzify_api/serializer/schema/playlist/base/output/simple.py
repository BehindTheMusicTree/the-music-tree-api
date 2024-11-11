from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.schema.playlist.base.output.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    LIB_TRACKS_COUNT = AvailableFields.LIB_TRACKS_COUNT
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = AvailableFields.NAME
    TYPE_LABEL = AvailableFields.TYPE_LABEL


class PlaylistSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
