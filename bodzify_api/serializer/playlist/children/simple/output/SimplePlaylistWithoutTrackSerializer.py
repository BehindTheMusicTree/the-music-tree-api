#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildSerializer \
    import PlaylistChildSerializer, FIELDS as PLAYLIST_CHILD_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    CREATED_ON = PLAYLIST_CHILD_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class SimplePlaylistWithoutTrackSerializer(PlaylistChildSerializer):
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT]
