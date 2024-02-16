#!/usr/bin/env python

from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL


class SimplePlaylistPostSchemaSerializer(InputModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [ATTRIBUTES_LABEL.NAME]
