#!/usr/bin/env python

from bodzify_api import settings
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.BasePlaylist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    NAME = PLAYLIST_ATTRIBUTES_LABEL.NAME


class SimplePlaylistSaveSchemaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LEN_MAX,
                                 required=False,
                                 allow_blank=True,
                                 allow_null=True)

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.NAME]
