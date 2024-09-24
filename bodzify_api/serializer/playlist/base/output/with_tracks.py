#!/usr/bin/env python

from bodzify_api.model.playlist.BasePlaylist import AttributesLabel, BasePlaylist
from bodzify_api.serializer.playlist.base.output.without_tracks \
    import BasePlaylistWithoutTracksSerializer, Fields as PARENT_FIELDS
from bodzify_api.serializer.playlist_lib_track_relation.output.without_playlist \
    import PlaylistLibTrackRelationWithoutPlaylist, Fields as PLAYLIST_LIB_TRACK_RELATION_FIELDS
from rest_framework import serializers


class Fields:
    UUID = PARENT_FIELDS.UUID
    NAME = PARENT_FIELDS.NAME
    TYPE = PARENT_FIELDS.TYPE
    CREATED_ON = PARENT_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = PARENT_FIELDS.LIB_TRACKS_COUNT
    LIB_TRACKS = AttributesLabel.LIB_TRACKS
    PLAY_COUNT = AttributesLabel.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = AttributesLabel.LAST_TRACK_LIST_UPDATE_DATE


class BasePlaylistWithTracksSerializer(BasePlaylistWithoutTracksSerializer):
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(
        source=AttributesLabel.PLAYLIST_LIB_TRACK_RELATIONS, many=True)
    library_tracks_count = serializers.IntegerField(source=f'{Fields.LIB_TRACKS}.count', read_only=True)

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.PLAY_COUNT,
                  Fields.LAST_TRACK_LIST_UPDATE_DATE]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[Fields.LIB_TRACKS] = sorted(
            representation[Fields.LIB_TRACKS], key=lambda x: x[PLAYLIST_LIB_TRACK_RELATION_FIELDS.POSITION])
        return representation
