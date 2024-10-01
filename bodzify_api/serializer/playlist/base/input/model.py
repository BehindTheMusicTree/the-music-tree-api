#!/usr/bin/env python

from bodzify_api.model.playlist.BasePlaylist import AttributesLabel as PlaylistAttributesLabels, BasePlaylist
from rest_framework import serializers


class Fields:
    USER = PlaylistAttributesLabels.USER


class BasePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.USER]
