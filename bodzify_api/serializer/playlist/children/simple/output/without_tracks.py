#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.child \
    import ChildPlaylistSerializer, Fields as CHILD_PLAYLIST_FIELDS


class Fields:
    UUID = CHILD_PLAYLIST_FIELDS.UUID
    NAME = CHILD_PLAYLIST_FIELDS.NAME
    CREATED_ON = CHILD_PLAYLIST_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = CHILD_PLAYLIST_FIELDS.LIB_TRACKS_COUNT


class SimplePlaylistWithoutTracksSerializer(ChildPlaylistSerializer):
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = SimplePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT]
