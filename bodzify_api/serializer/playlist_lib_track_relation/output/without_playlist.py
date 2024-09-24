#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.output.without_playlists_and_album \
    import LibTrackWithoutAlbumAndPlaylistSerializer
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation, AttributesLabel


class Fields:
    LIB_TRACK = AttributesLabel.LIB_TRACK
    CREATED_ON = AttributesLabel.CREATED_ON
    POSITION = AttributesLabel.POSITION


class PlaylistLibTrackRelationWithoutPlaylist(serializers.ModelSerializer):
    library_track = LibTrackWithoutAlbumAndPlaylistSerializer()

    class Meta:
        model = PlaylistLibTrackRelation
        fields = [Fields.LIB_TRACK,
                  Fields.CREATED_ON,
                  Fields.POSITION]
