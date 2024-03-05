#!/usr/bin/env python

from bodzify_api.model.playlist.SimplePlaylist \
    import SimplePlaylist, ATTRIBUTES_LABELS as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class FIELDS:
    PLAYLIST = SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.PLAYLIST
    NAME = SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.NAME


class SimplePlaylistSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.PLAYLIST,
                  FIELDS.NAME]
