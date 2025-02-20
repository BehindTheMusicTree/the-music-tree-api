from rest_framework import serializers

from bodzify_api.model.album.Album import Album
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.album.Fields import Fields as AvailableFields
from bodzify_api.serializer.model.artist.minimum import ArtistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    ALBUM_ARTISTS = AvailableFields.ALBUM_ARTISTS


class AlbumMinimumSerializer(AppSerializer, serializers.ModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUM_ARTISTS]
