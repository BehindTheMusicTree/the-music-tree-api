
from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.serializer.model.playlist.base.output.simple import PlaylistSimpleSerializer


class Fields:
    UUID = PlayListFields.UUID
    NAME = PlayListFields.NAME_PUBLIC
    CREATED_ON = PlayListFields.CREATED_ON
    UPDATED_ON = PlayListFields.UPDATED_ON
    LIB_TRACKS_NOT_ARCHIVED_INTERNAL = PlayListFields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_PUBLIC = PlayListFields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = PlayListFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = PlayListFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    LIB_TRACK_PLAYLIST_RELS_INTERNAL = PlayListFields.LIB_TRACK_PLAYLIST_RELS_INTERNAL
    LIB_TRACK_PLAYLIST_RELS_PUBLIC = PlayListFields.LIB_TRACK_PLAYLIST_RELS_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = PlayListFields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = PlayListFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = PlayListFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlayListFields.DURATION_STR_IN_HOUR_MIN_SEC
    LAST_TRACK_LIST_UPDATE_DATE = PlayListFields.LAST_TRACK_LIST_UPDATE_DATE


class ChildPlaylistSerializer(PlaylistSimpleSerializer):
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks = serializers.ListField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL)

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
