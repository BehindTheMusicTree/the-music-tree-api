from rest_framework import serializers

from api.model.playlist.Playlist import Playlist
from api.serializer.field.AppCharField import AppCharField
from api.serializer.model.playlist.base.output.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = AvailableFields.NAME
    TYPE_LABEL_INTERNAL = AvailableFields.TYPE_LABEL_INTERNAL
    TYPE_LABEL_PUBLIC = AvailableFields.TYPE_LABEL_PUBLIC
    CREATED_ON = AvailableFields.CREATED_ON


class PlaylistSimpleSerializer(serializers.ModelSerializer):
    type = AppCharField(source=Fields.TYPE_LABEL_INTERNAL)
    uploaded_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL_PUBLIC,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON]
