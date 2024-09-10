#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.child \
    import ChildPlaylistSerializer, FIELDS as CHILD_PLAYLIST_FIELDS


class FIELDS:
    UUID = CHILD_PLAYLIST_FIELDS.UUID
    NAME = CHILD_PLAYLIST_FIELDS.NAME
    CREATED_ON = CHILD_PLAYLIST_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = CHILD_PLAYLIST_FIELDS.LIB_TRACKS_COUNT


class SimplePlaylistWithoutTracksSerializer(ChildPlaylistSerializer):
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT]
