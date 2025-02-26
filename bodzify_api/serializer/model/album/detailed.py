from rest_framework import serializers

from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.model.album.Fields import Fields
from bodzify_api.serializer.model.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.model.lib_track.output.simple.simple_without_album_with_track_number import (
    LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer
)


class AlbumDetailedSerializer(serializers.ModelSerializer):
    library_tracks_sorted = LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(
        source=Fields.LIB_TRACKS_NOT_ARCHIVED_SORTED_INTERNAL, many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL)
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME_PUBLIC,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_SORTED_PUBLIC,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
