#!/usr/bin/env python

from bodzify_api.model.playlist.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import \
    ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import \
    FOREIGN_MODEL_ATTRIBUTES_LABEL as PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import \
    FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithoutTracksSerializer import \
    CriteriaPlaylistWithoutTracksSerializer
from bodzify_api.serializer.track.output.LibTrackWithoutAlbumAndPlaylistSerializer import \
    LibTrackWithoutAlbumAndPlaylistSerializer


class CriteriaPlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):
    library_tracks = LibTrackWithoutAlbumAndPlaylistSerializer(
        source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.LIBRARY_TRACKS, many=True)

    class Meta:
        model = CriteriaPlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS]
