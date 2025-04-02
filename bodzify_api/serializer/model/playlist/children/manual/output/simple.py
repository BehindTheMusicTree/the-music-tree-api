from rest_framework import serializers

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.field.AppCharField import AppCharField

from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = AvailableFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    CREATED_ON = AvailableFields.CREATED_ON


class ManualPlaylistSimpleSerializer(serializers.ModelSerializer):
    name = AppCharField()
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON]
