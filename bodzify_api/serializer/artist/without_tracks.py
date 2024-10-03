#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.album.without_tracks import AlbumWithoutTracksSerializer
from bodzify_api.model.Artist import Artist, AttributesLabels


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    ALBUMS = AttributesLabels.ALBUMS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_COUNT_ARCHIVED = AttributesLabels.LIB_TRACKS_COUNT_ARCHIVED
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC


class ArtistWithoutTracksSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksSerializer(many=True)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_COUNT_ARCHIVED,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
