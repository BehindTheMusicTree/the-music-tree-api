#!/usr/bin/env python

from bodzify_api.model.playlist.BasePlaylist import ATTRIBUTES_LABEL, BasePlaylist
from bodzify_api.serializer.playlist.base.output.without_tracks \
    import BasePlaylistWithoutTracksSerializer, FIELDS as PARENT_FIELDS
from bodzify_api.serializer.playlist_lib_track_relation.output.without_playlist \
    import PlaylistLibTrackRelationWithoutPlaylist, FIELDS as PLAYLIST_LIB_TRACK_RELATION_FIELDS
from rest_framework import serializers


class FIELDS:
    UUID = PARENT_FIELDS.UUID
    NAME = PARENT_FIELDS.NAME
    TYPE = PARENT_FIELDS.TYPE
    CREATED_ON = PARENT_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = PARENT_FIELDS.LIB_TRACKS_COUNT
    LIB_TRACKS = ATTRIBUTES_LABEL.LIB_TRACKS
    PLAY_COUNT = ATTRIBUTES_LABEL.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ATTRIBUTES_LABEL.LAST_TRACK_LIST_UPDATE_DATE


class BasePlaylistWithTracksSerializer(BasePlaylistWithoutTracksSerializer):
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(
        source=ATTRIBUTES_LABEL.PLAYLIST_LIB_TRACK_RELATIONS, many=True)
    library_tracks_count = serializers.IntegerField(source=f'{FIELDS.LIB_TRACKS}.count', read_only=True)

    class Meta:
        model = BasePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.TYPE,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS,
                  FIELDS.PLAY_COUNT,
                  FIELDS.LAST_TRACK_LIST_UPDATE_DATE]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[FIELDS.LIB_TRACKS] = sorted(
            representation[FIELDS.LIB_TRACKS], key=lambda x: x[PLAYLIST_LIB_TRACK_RELATION_FIELDS.POSITION])
        return representation
