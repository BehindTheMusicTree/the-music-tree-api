#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildWithoutTrackSerializer \
    import PlaylistChildWithoutTrackSerializer, FIELDS as PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.UUID
    NAME = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.ADDED_ON
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.LIB_TRACKS_COUNT


class SimplePlaylistWithoutTrackSerializer(PlaylistChildWithoutTrackSerializer):
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS_COUNT]
