from rest_framework import serializers

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.model.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.model.lib_track.output.simple.simple_without_artist import \
    LibTrackSimpleWithoutPlaylistAndArtistSerializer

from .Fields import Fields


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumMinimumSerializer(many=True)
    library_tracks = LibTrackSimpleWithoutPlaylistAndArtistSerializer(
        source=Fields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME_PUBLIC,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
