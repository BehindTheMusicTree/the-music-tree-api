#!/usr/bin/env python
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL


class SimplePlaylistPostSerializer(InputSerializer):

    class Meta:
        model = GenrePlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.NAME]
