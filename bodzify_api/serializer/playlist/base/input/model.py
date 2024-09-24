#!/usr/bin/env python

from bodzify_api.model.playlist.BasePlaylist import AttributesLabel as PLAYLIST_ATTRIBUTES_LABEL, BasePlaylist
from rest_framework import serializers


class Fields:
    USER = PLAYLIST_ATTRIBUTES_LABEL.USER


class BasePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.USER]
