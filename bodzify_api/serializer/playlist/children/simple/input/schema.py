#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import \
    AttributesLabels as BaseAttributesLabels
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist


class Fields:
    NAME = BaseAttributesLabels.NAME


class SimplePlaylistSchemaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LEN_MAX,
                                 required=False,
                                 allow_blank=True,
                                 allow_null=True)

    class Meta:
        model = SimplePlaylist
        fields = [Fields.NAME]
