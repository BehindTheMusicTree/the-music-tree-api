#!/usr/bin/env python
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class AlbumWithoutTracksSerializer(serializers.ModelSerializer):
    albumArtists = ArtistWithOnlyNameSerializer(many=True)
    trackCount = serializers.IntegerField(source='librarytrack_set.count')
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj) -> float:
        value = LibraryTrack.objects.filter(album=obj).aggregate(
                duration=Sum(Album.ATTRIBUTE_DURATION_LABEL))
        return value[Album.ATTRIBUTE_DURATION_LABEL]

    class Meta:
        model = Album
        fields = [
            Album.ATTRIBUTE_UUID_LABEL,
            Album.ATTRIBUTE_NAME_LABEL,
            Album.ATTRIBUTE_YEAR_LABEL,
            Album.ATTRIBUTE_TRACK_COUNT_LABEL,
            Album.ATTRIBUTE_DURATION_LABEL,
            Album.ATTRIBUTE_ALBUM_ARTISTS_LABEL,
        ]
