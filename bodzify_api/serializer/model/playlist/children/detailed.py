
from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.serializer.model.playlist.base.output.simple import PlaylistSimpleSerializer


class Fields:
    UUID = PlayListFields.UUID
    NAME = PlayListFields.NAME_PUBLIC
    CREATED_ON = PlayListFields.CREATED_ON
    UPDATED_ON = PlayListFields.UPDATED_ON
    UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL = PlayListFields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL
    UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC = PlayListFields.UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC
    UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL = PlayListFields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC = PlayListFields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = PlayListFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlayListFields.DURATION_STR_IN_HOUR_MIN_SEC


class ChildPlaylistSerializer(PlaylistSimpleSerializer):
    library_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks = serializers.ListField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        fields = [Fields.UUID,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.NAME,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
