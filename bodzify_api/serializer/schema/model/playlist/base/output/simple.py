from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as ModelFields
from bodzify_api.serializer.schema.model.playlist.base.output.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    LIB_TRACKS_COUNT = AvailableFields.LIB_TRACKS_COUNT
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = AvailableFields.NAME
    TYPE_LABEL_USER_FRIENDLY = AvailableFields.TYPE_LABEL_USER_FRIENDLY
    CREATED_ON = AvailableFields.CREATED_ON


class PlaylistSimpleSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source=ModelFields.TYPE_LABEL)

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL_USER_FRIENDLY,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON]
