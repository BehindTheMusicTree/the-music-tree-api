#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.LibTrackPlaylistPositionRel import AttributesLabels, LibTrackPlaylistPositionRel
from bodzify_api.serializer.track.output.simple_without_playlists_and_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    LIB_TRACK = AttributesLabels.LIB_TRACK
    CREATED_ON = AttributesLabels.CREATED_ON
    UPDATED_ON = AttributesLabels.UPDATED_ON
    POSITION = AttributesLabels.POSITION


class LibTrackPlaylistPositionRelWithLibTrackAndPosition(serializers.ModelSerializer):
    library_track = LibTrackSimpleWithoutPlaylistAndAlbumSerializer()

    class Meta:
        model = LibTrackPlaylistPositionRel
        fields = [Fields.LIB_TRACK, Fields.CREATED_ON, Fields.POSITION]
