#!/usr/bin/env python

from bodzify_api import settings
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.BasePlaylist import AttributesLabel as PLAYLIST_ATTRIBUTES_LABEL
from rest_framework import serializers


class Fields:
    NAME = PLAYLIST_ATTRIBUTES_LABEL.NAME


class SimplePlaylistSchemaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LEN_MAX,
                                 required=False,
                                 allow_blank=True,
                                 allow_null=True)

    class Meta:
        model = SimplePlaylist
        fields = [Fields.NAME]
