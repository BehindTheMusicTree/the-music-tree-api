#!/usr/bin/env python
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLLAYLIST_ATTRIBUTES_LABEL


class SimplePlaylistSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [PLLAYLIST_ATTRIBUTES_LABEL.USER,
                  PLLAYLIST_ATTRIBUTES_LABEL.NAME]
