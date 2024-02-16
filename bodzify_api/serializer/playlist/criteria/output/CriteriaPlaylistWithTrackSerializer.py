#!/usr/bin/env python

from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist, \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import \
    FOREIGN_MODEL_ATTRIBUTES_LABEL as PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithoutTracksSerializer import \
    CriteriaPlaylistWithoutTracksSerializer
from bodzify_api.serializer.track.output.TrackWithoutPlaylistsSerializer import \
    TrackWithoutPlaylistsSerializer


class CriteriaPlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):
    library_tracks = TrackWithoutPlaylistsSerializer(source='playlist__librarytrack_set', read_only=True, many=True)

    class Meta:
        model = CriteriaPlaylist
        fields = [PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.UUID,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.ADDED_ON,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.TRACK_COUNT,
                  PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL.LIBRARY_TRACKS]
