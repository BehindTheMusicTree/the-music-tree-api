#!/usr/bin/env python

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL


class FIELDS:
    NAME = PLAYLIST_ATTRIBUTES_LABEL.NAME


class SimplePlaylistPostSchemaSerializer(InputEndpointSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.NAME]
