from rest_framework import serializers

from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.serializer.field.AppCharField import AppCharField

from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    CREATED_ON = AvailableFields.CREATED_ON


class ManualPlaylistSimpleSerializer(serializers.ModelSerializer):
    name = AppCharField()
    uploaded_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON]
