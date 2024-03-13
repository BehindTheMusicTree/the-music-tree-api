#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL, Playlist
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer import PlaylistWithoutTrackSerializer
from bodzify_api.serializer.track.output.LibTrackWithoutPlaylistsSerializer import LibTrackWithoutPlaylistsSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    LIBRARY_TRACKS_COUNT = ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT
    LIBRARY_TRACKS = ATTRIBUTES_LABEL.LIBRARY_TRACKS


class PlaylistWithTracksSerializer(PlaylistWithoutTrackSerializer):
    library_tracks = LibTrackWithoutPlaylistsSerializer(many=True)

    class Meta:
        model = Playlist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.LIBRARY_TRACKS_COUNT,
                  FIELDS.LIBRARY_TRACKS]
