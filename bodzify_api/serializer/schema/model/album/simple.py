
from rest_framework import serializers

from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.schema.model.album.fields import Fields
from bodzify_api.serializer.schema.model.artist.minimum import ArtistMinimumSerializer


class AlbumSimpleSerializer(serializers.ModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
