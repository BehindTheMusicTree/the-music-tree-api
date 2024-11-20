from rest_framework import serializers

from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.schema.model.album.fields import Fields
from bodzify_api.serializer.schema.model.artist.minimum import ArtistMinimumSerializer
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album_with_position_in_album \
    import LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer


class AlbumDetailedSerializer(serializers.ModelSerializer):
    library_tracks = serializers.SerializerMethodField()
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

    def get_library_tracks(self, instance: Album):
        sorted_tracks = instance.lib_tracks_sorted
        return LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(sorted_tracks, many=True).data
