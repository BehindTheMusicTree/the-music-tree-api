#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, ATTRIBUTES_LABEL as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.BasePlaylist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    BASE_PLAYLIST = SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.BASE_PLAYLIST
    NAME = SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.NAME
    USER = PLAYLIST_ATTRIBUTES_LABEL.USER


class SimplePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.BASE_PLAYLIST,
                  FIELDS.NAME]
