
from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.schema.playlist.base.output.fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    LIB_TRACKS_COUNT = AvailableFields.LIB_TRACKS_COUNT
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = AvailableFields.NAME
    TYPE_LABEL = AvailableFields.TYPE_LABEL


class BasePlaylistSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
