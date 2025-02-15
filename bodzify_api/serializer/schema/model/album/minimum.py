from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer
from bodzify_api.serializer.schema.model.album.Fields import Fields as AvailableFields
from bodzify_api.serializer.schema.model.artist.minimum import ArtistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    ALBUM_ARTISTS = AvailableFields.ALBUM_ARTISTS


class AlbumMinimumSerializer(AppModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUM_ARTISTS]
