#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer
)
from bodzify_api.serializer.track.LibraryTrackWithoutPlaylistsResponseSerializer import (
    LibraryTrackWithoutPlaylistsResponseSerializer
) 


class PlaylistWithTrackSerializer(PlaylistWithoutTracksSerializer):
    libraryTracks = LibraryTrackWithoutPlaylistsResponseSerializer(
        source='librarytrack_set', read_only=True, many=True)

    class Meta:
        model = Playlist    
        fields = [
            "uuid",
            "name",
            "type",
            "criteria",
            "parent",
            "addedOn",
            "trackCount",
            "libraryTracks"
        ]
