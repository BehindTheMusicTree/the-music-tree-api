#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, \
    ATTRIBUTES_LABELS as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.output.PlaylistWithoutParentSerializer import PlaylistSerializer


class SimplePlaylistWithoutParentSerializer(PlaylistSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT]
