#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, \
    ATTRIBUTES_LABELS as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.output.PlaylistChildWithoutTrackSerializer import PlaylistChildWithoutTrackSerializer


class FIELDS:
    UUID = PLAYLIST_ATTRIBUTES_LABEL.UUID
    NAME = SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.NAME
    ADDED_ON = PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON
    LIBRARY_TRACKS_COUNT = PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT


class SimplePlaylistWithoutTrackSerializer(PlaylistChildWithoutTrackSerializer):

    class Meta:
        model = SimplePlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.LIBRARY_TRACKS_COUNT]
