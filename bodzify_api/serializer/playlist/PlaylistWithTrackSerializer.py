#!/usr/bin/env python
from bodzify_api.model.playlist.Playlist import Playlist, ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import \
    PlaylistWithoutTracksSerializer
from bodzify_api.serializer.track.output.TrackWithoutPlaylistsSerializer import \
    TrackWithoutPlaylistsSerializer


class PlaylistWithTracksSerializer(PlaylistWithoutTracksSerializer):
    libraryTracks = TrackWithoutPlaylistsSerializer(
        source='librarytrack_set', read_only=True, many=True)

    class Meta:
        model = Playlist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ADDED_ON,
                  "trackCount",
                  "libraryTracks"]
