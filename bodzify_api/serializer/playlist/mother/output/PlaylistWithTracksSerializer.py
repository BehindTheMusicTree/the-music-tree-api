#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL, Playlist
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer \
    import PlaylistWithoutTrackSerializer, FIELDS as PARENT_FIELDS
from bodzify_api.serializer.track.output.LibTrackWithoutPlaylistsSerializer import LibTrackWithoutPlaylistsSerializer


class FIELDS:
    UUID = PARENT_FIELDS.UUID
    NAME = PARENT_FIELDS.NAME
    TYPE = PARENT_FIELDS.TYPE
    ADDED_ON = PARENT_FIELDS.ADDED_ON
    LIB_TRACKS_COUNT = PARENT_FIELDS.LIB_TRACKS_COUNT
    LIB_TRACKS = ATTRIBUTES_LABEL.LIB_TRACKS


class PlaylistWithTracksSerializer(PlaylistWithoutTrackSerializer):
    library_tracks = LibTrackWithoutPlaylistsSerializer(many=True)

    class Meta:
        model = Playlist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.TYPE,
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS]
