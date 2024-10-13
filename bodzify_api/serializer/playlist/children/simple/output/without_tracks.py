#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.child import \
    ChildPlaylistSerializer
from bodzify_api.serializer.playlist.children.child import \
    Fields as ChildPlaylistFields


class Fields:
    UUID = ChildPlaylistFields.UUID
    NAME = ChildPlaylistFields.NAME
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT


class SimplePlaylistWithoutTracksSerializer(ChildPlaylistSerializer):
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = SimplePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT]
