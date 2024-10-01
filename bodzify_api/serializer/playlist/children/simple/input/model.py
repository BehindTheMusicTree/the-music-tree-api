#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, AttributesLabel as SIMPLE_PlaylistAttributesLabels
from bodzify_api.model.playlist.BasePlaylist import AttributesLabel as PlaylistAttributesLabels
from rest_framework import serializers


class Fields:
    BASE_PLAYLIST = SIMPLE_PlaylistAttributesLabels.BASE_PLAYLIST
    NAME = SIMPLE_PlaylistAttributesLabels.NAME
    USER = PlaylistAttributesLabels.USER


class SimplePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [Fields.BASE_PLAYLIST,
                  Fields.NAME]
