from rest_framework import serializers

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.serializer.schema.artist.fields import Fields
from bodzify_api.serializer.schema.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.schema.lib_track.output.simple.simple_without_artist \
    import LibTrackSimpleWithoutPlaylistAndArtistSerializer


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumMinimumSerializer(many=True)
    library_tracks = LibTrackSimpleWithoutPlaylistAndArtistSerializer(
        source=ArtistFields.LIB_TRACKS_NOT_ARCHIVED, many=True)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
