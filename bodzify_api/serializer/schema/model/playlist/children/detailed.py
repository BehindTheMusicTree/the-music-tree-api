
from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.serializer.schema.model.playlist.base.output.simple import PlaylistSimpleSerializer


class Fields:
    UUID = PlaylistFields.UUID
    NAME = PlaylistFields.NAME_PUBLIC
    CREATED_ON = PlaylistFields.CREATED_ON
    UPDATED_ON = PlaylistFields.UPDATED_ON
    LIB_TRACKS_NOT_ARCHIVED_INTERNAL = PlaylistFields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_PUBLIC = PlaylistFields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = PlaylistFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = PlaylistFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = PlaylistFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = PlaylistFields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL
    DURATION_IN_SEC = PlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC


class ChildPlaylistSerializer(PlaylistSimpleSerializer):
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC)
    library_tracks = serializers.ListField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC)

    class Meta:
        fields = [Fields.UUID,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.NAME,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
