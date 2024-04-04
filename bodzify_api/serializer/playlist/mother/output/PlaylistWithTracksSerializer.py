#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL, Playlist
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer \
    import PlaylistWithoutTrackSerializer, FIELDS as PARENT_FIELDS
from bodzify_api.serializer.playlist_library_track.output.PlaylistLibTrackRelationWithoutPlaylist import PlaylistLibTrackRelationWithoutPlaylist
from rest_framework import serializers


class FIELDS:
    UUID = PARENT_FIELDS.UUID
    NAME = PARENT_FIELDS.NAME
    TYPE = PARENT_FIELDS.TYPE
    ADDED_ON = PARENT_FIELDS.ADDED_ON
    LIB_TRACKS_COUNT = PARENT_FIELDS.LIB_TRACKS_COUNT
    LIB_TRACKS = ATTRIBUTES_LABEL.LIB_TRACKS
    PLAY_COUNT = ATTRIBUTES_LABEL.PLAY_COUNT


class PlaylistWithTracksSerializer(PlaylistWithoutTrackSerializer):
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(source=ATTRIBUTES_LABEL.PLAYLIST_LIB_TRACK_RELATIONS,
                                                             many=True)
    library_tracks_count = serializers.IntegerField(source=f'{FIELDS.LIB_TRACKS}.count', read_only=True)

    class Meta:
        model = Playlist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.TYPE,
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS,
                  FIELDS.PLAY_COUNT]
