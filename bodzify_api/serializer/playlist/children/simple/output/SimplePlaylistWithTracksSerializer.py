#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildSerializer \
    import PlaylistChildSerializer, FIELDS as PLAYLIST_CHILD_FIELDS
from bodzify_api.serializer.playlist_library_track.output.PlaylistLibTrackRelationWithoutPlaylist import PlaylistLibTrackRelationWithoutPlaylist
from rest_framework import serializers


class FIELDS:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_FIELDS.ADDED_ON
    LIB_TRACKS = PLAYLIST_CHILD_FIELDS.LIB_TRACKS
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class SimplePlaylistWithTracksSerializer(PlaylistChildSerializer):
    name = serializers.CharField()  # Overriding the name field of the parent class
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(source='playlist.playlistlibrarytrack_set', many=True)

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  'name',
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS]
