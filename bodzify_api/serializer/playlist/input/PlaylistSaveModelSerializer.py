#!/usr/bin/env python

from bodzify_api.serializer.InputModelSerializer import InputModelSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, Playlist


class FIELDS:
    USER = PLAYLIST_ATTRIBUTES_LABEL.USER


class PlaylistSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = Playlist
        fields = [FIELDS.USER]
