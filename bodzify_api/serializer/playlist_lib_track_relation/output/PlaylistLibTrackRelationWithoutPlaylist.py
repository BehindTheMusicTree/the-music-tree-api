#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.output.LibTrackWithoutAlbumAndPlaylistSerializer \
    import LibTrackWithoutAlbumAndPlaylistSerializer
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation, ATTRIBUTES_LABEL


class FIELDS:
    LIB_TRACK = ATTRIBUTES_LABEL.LIB_TRACK
    CREATED_ON = ATTRIBUTES_LABEL.CREATED_ON
    POSITION = ATTRIBUTES_LABEL.POSITION


class PlaylistLibTrackRelationWithoutPlaylist(serializers.ModelSerializer):
    library_track = LibTrackWithoutAlbumAndPlaylistSerializer()

    class Meta:
        model = PlaylistLibTrackRelation
        fields = [FIELDS.LIB_TRACK,
                  FIELDS.CREATED_ON,
                  FIELDS.POSITION]
