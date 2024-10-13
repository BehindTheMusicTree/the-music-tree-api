#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.LibTrackPlaylistPositionRel import AttributesLabels, LibTrackPlaylistPositionRel
from bodzify_api.serializer.album.with_only_name_and_artists import AlbumWithOnlyNameAndArtistsSerializer
from bodzify_api.serializer.track.output.without_playlists_and_album import LibTrackWithoutAlbumAndPlaylistSerializer


class Fields:
    LIB_TRACK_MIXIN = AttributesLabels.BASE_PLAYLIST
    POSITION = AttributesLabels.POSITION


class AlbumLibTrackPlaylistPositionRelWithoutLibTrack(serializers.ModelSerializer):
    lib_track_mixin = AlbumWithOnlyNameAndArtistsSerializer()

    class Meta:
        model = LibTrackPlaylistPositionRel
        fields = [Fields.LIB_TRACK_MIXIN, Fields.POSITION]
