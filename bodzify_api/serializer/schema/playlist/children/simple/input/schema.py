#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import Fields as BasePlaylistFields
from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist


class Fields:
    NAME = BasePlaylistFields.NAME


class ManualPlaylistSchemaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX,
                                 required=False,
                                 allow_blank=True,
                                 allow_null=True)

    class Meta:
        model = ManualPlaylist
        fields = [Fields.NAME]
