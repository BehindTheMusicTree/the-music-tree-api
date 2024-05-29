#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.child \
    import PlaylistChildSerializer, FIELDS as PLAYLIST_CHILD_FIELDS
from bodzify_api.serializer.playlist_lib_track_relation.output.without_playlist import PlaylistLibTrackRelationWithoutPlaylist
from rest_framework import serializers


class FIELDS:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    CREATED_ON = PLAYLIST_CHILD_FIELDS.CREATED_ON
    LIB_TRACKS = PLAYLIST_CHILD_FIELDS.LIB_TRACKS
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class SimplePlaylistWithTracksSerializer(PlaylistChildSerializer):
    name = serializers.CharField()  # Overriding the name field of the parent class
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(source='playlist.playlist_lib_track_relation_relations',
                                                             many=True)

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS]
