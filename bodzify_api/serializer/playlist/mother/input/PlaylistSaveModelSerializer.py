#!/usr/bin/env python

from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, Playlist


class FIELDS:
    USER = PLAYLIST_ATTRIBUTES_LABEL.USER


class PlaylistSaveModelSerializer(InputEndpointSerializer):

    class Meta:
        model = Playlist
        fields = [FIELDS.USER]
