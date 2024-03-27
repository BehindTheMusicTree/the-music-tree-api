#!/usr/bin/env python
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class FIELDS:
    UUID = ALBUM_ATTRIBUTES_LABEL.UUID
    NAME = ALBUM_ATTRIBUTES_LABEL.NAME
    YEAR = ALBUM_ATTRIBUTES_LABEL.YEAR
    ALBUM_ARTISTS = ALBUM_ATTRIBUTES_LABEL.ALBUM_ARTISTS
    LIB_TRACKS_COUNT = ALBUM_ATTRIBUTES_LABEL.LIB_TRACKS_COUNT
    DURATION = ALBUM_ATTRIBUTES_LABEL.DURATION


class AlbumWithoutTracksSerializer(serializers.ModelSerializer):
    album_artists = ArtistWithOnlyNameSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=ALBUM_ATTRIBUTES_LABEL.LIB_TRACKS + '.count')
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj) -> float:
        value = LibraryTrack.objects.filter(album=obj).aggregate(duration=Sum(ALBUM_ATTRIBUTES_LABEL.DURATION))
        return value[ALBUM_ATTRIBUTES_LABEL.DURATION]

    class Meta:
        model = Album
        fields = [
            FIELDS.UUID,
            FIELDS.NAME,
            FIELDS.YEAR,
            FIELDS.ALBUM_ARTISTS,
            FIELDS.LIB_TRACKS_COUNT,
            FIELDS.DURATION,
        ]
