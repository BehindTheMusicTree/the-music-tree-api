#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Album import Album
from bodzify_api.model.Album import AttributesLabels as AlbumAttributesLabels
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer


class Fields:
    UUID = AlbumAttributesLabels.UUID
    NAME = AlbumAttributesLabels.NAME
    ALBUM_ARTISTS = AlbumAttributesLabels.ALBUM_ARTISTS


class AlbumWithOnlyNameAndArtistsSerializer(serializers.ModelSerializer):
    album_artists = ArtistWithOnlyNameSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID, Fields.NAME, Fields.ALBUM_ARTISTS]
