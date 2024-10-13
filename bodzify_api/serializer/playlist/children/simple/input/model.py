#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import AttributesLabels as BaseAttributesLabels
from bodzify_api.model.playlist.children.SimplePlaylist import AttributesLabels, SimplePlaylist


class Fields:
    BASE_PLAYLIST = AttributesLabels.BASE_PLAYLIST
    NAME = AttributesLabels.NAME
    USER = BaseAttributesLabels.USER


class SimplePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [Fields.BASE_PLAYLIST,
                  Fields.NAME]
