#!/usr/bin/env python


from rest_framework import serializers
from bodzify_api.model.Album import Album, AttributesLabels as AttributesLabels
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    YEAR = AttributesLabels.YEAR
    ALBUM_ARTISTS = AttributesLabels.ALBUM_ARTISTS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumWithoutTracksSerializer(serializers.ModelSerializer):
    album_artists = ArtistWithOnlyNameSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
