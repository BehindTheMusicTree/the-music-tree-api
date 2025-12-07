from rest_framework import serializers

from api.model.album.Album import Album
from api.serializer.AppInputSerializer import AppInputSerializer
from api.serializer.model.album.Fields import Fields as AvailableFields
from api.serializer.model.artist.minimum import ArtistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME_PUBLIC
    ALBUM_ARTISTS = AvailableFields.ALBUM_ARTISTS


class AlbumMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUM_ARTISTS]
