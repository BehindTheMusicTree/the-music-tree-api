#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildWithoutTrackSerializer \
    import PlaylistChildWithoutTrackSerializer, FIELDS as PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.UUID
    NAME = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.ADDED_ON
    LIBRARY_TRACKS_COUNT = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.LIBRARY_TRACKS_COUNT


class SimplePlaylistWithoutTrackSerializer(PlaylistChildWithoutTrackSerializer):
    name = serializers.CharField()  # only to override the mothers one

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.LIBRARY_TRACKS_COUNT]
