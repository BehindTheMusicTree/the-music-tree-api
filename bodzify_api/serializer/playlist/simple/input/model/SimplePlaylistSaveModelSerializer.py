#!/usr/bin/env python
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL


class SimplePlaylistSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [ATTRIBUTES_LABEL.USER,
                  ATTRIBUTES_LABEL.NAME]
