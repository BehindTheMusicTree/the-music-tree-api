#!/usr/bin/env python
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class AlbumWithoutTracksSerializer(serializers.ModelSerializer):
    albumArtists = ArtistWithOnlyNameSerializer(many=True)
    trackCount = serializers.IntegerField(source='librarytrack_set.count')
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj) -> float:
        value = LibraryTrack.objects.filter(album=obj).aggregate(
                duration=Sum(ALBUM_ATTRIBUTES_LABEL.DURATION))
        return value[ALBUM_ATTRIBUTES_LABEL.DURATION]

    class Meta:
        model = Album
        fields = [
            ALBUM_ATTRIBUTES_LABEL.UUID,
            ALBUM_ATTRIBUTES_LABEL.NAME,
            ALBUM_ATTRIBUTES_LABEL.YEAR,
            ALBUM_ATTRIBUTES_LABEL.ALBUM_ARTISTS,
            ALBUM_ATTRIBUTES_LABEL.TRACK_COUNT,
            ALBUM_ATTRIBUTES_LABEL.DURATION,
        ]
