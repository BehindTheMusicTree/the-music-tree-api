#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Album import Album
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.album.fields import Fields
from bodzify_api.serializer.schema.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.track.output.simple.simple_without_album_with_position_in_album \
    import LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer


class AlbumDetailedSerializer(serializers.ModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]

    def to_representation(self, instance: Album):
        representation = super().to_representation(instance)
        sorted_tracks = LibraryTrack.get_sorted_tracks(instance.library_tracks.all())
        representation[Fields.LIB_TRACKS] = LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(
            sorted_tracks, many=True).data
        return representation
