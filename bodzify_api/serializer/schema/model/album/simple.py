
from dbm.ndbm import library
from rest_framework import serializers

from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.schema.model.album.fields import Fields
from bodzify_api.serializer.schema.model.artist.minimum import ArtistMinimumSerializer


class AlbumSimpleSerializer(serializers.ModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON]
