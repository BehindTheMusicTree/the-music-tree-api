#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.output.LibTrackWithoutAlbumAndPlaylistSerializer \
    import LibTrackWithoutAlbumAndPlaylistSerializer
from bodzify_api.model.PlaylistLibraryTrack import PlaylistLibraryTrack, ATTRIBUTES_LABEL


class FIELDS:
    LIB_TRACK = ATTRIBUTES_LABEL.LIB_TRACK
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    POSITION = ATTRIBUTES_LABEL.POSITION


class PlaylistLibraryTrackWithoutPlaylist(serializers.ModelSerializer):
    library_track = LibTrackWithoutAlbumAndPlaylistSerializer()

    class Meta:
        model = PlaylistLibraryTrack
        fields = [FIELDS.LIB_TRACK,
                  FIELDS.ADDED_ON,
                  FIELDS.POSITION]
