#!/usr/bin/env python
from bodzify_api.serializer.track.output.TrackWithoutPlaylistsAndGenreSerializer import TrackWithoutPlaylistsAndGenreSerializer
from bodzify_api.model.playlist.Playlist import Playlist, ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithoutTracksSerializer import \
    CriteriaPlaylistWithoutTracksSerializer


class GenrePlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):
    libraryTracks = TrackWithoutPlaylistsAndGenreSerializer(
        source='librarytrack_set', read_only=True, many=True)

    class Meta:
        model = Playlist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ADDED_ON,
                  ATTRIBUTES_LABEL.PARENT,
                  "trackCount",
                  "libraryTracks"]
