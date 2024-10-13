#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import \
    AttributesLabels as BaseAttributesLabels
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist


class Fields:
    USER = BaseAttributesLabels.USER


class BasePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.USER]
