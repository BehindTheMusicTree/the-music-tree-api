
from rest_framework import serializers

from api.model.playlist.Fields import Fields as PlayListFields
from api.serializer.model.playlist.base.output.simple import PlaylistSimpleSerializer


class Fields:
    UUID = PlayListFields.UUID
    NAME = PlayListFields.NAME_PUBLIC
    CREATED_ON = PlayListFields.CREATED_ON
    UPDATED_ON = PlayListFields.UPDATED_ON
    TRACKS_NOT_ARCHIVED_INTERNAL = PlayListFields.TRACKS_NOT_ARCHIVED_INTERNAL
    TRACKS_NOT_ARCHIVED_PUBLIC = PlayListFields.TRACKS_NOT_ARCHIVED_PUBLIC
    TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = PlayListFields.TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = PlayListFields.TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    TRACK_PLAYLIST_RELS_INTERNAL = PlayListFields.TRACK_PLAYLIST_RELS_INTERNAL
    TRACK_PLAYLIST_RELS_PUBLIC = PlayListFields.TRACK_PLAYLIST_RELS_PUBLIC
    TRACKS_ARCHIVED_COUNT_INTERNAL = PlayListFields.TRACKS_ARCHIVED_COUNT_INTERNAL
    TRACKS_ARCHIVED_COUNT_PUBLIC = PlayListFields.TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = PlayListFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlayListFields.DURATION_STR_IN_HOUR_MIN_SEC


class ChildPlaylistSerializer(PlaylistSimpleSerializer):
    tracks_count = serializers.IntegerField(source=Fields.TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    tracks = serializers.ListField(source=Fields.TRACKS_NOT_ARCHIVED_INTERNAL)
    tracks_archived_count = serializers.IntegerField()

    class Meta:
        fields = [Fields.UUID,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.NAME,
                  Fields.TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
