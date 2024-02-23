#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, \
    FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, \
    ATTRIBUTES_LABELS as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.simple.output.SimplePlaylistWithoutTrackSerializer import \
    SimplePlaylistWithoutTrackSerializer
from bodzify_api.serializer.track.output.LibTrackWithoutAlbumAndPlaylistSerializer import \
    LibTrackWithoutAlbumAndPlaylistSerializer


class SimplePlaylistWithTracksSerializer(SimplePlaylistWithoutTrackSerializer):
    library_tracks = LibTrackWithoutAlbumAndPlaylistSerializer(
        source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.LIBRARY_TRACKS, many=True)

    class Meta:
        model = SimplePlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS]
