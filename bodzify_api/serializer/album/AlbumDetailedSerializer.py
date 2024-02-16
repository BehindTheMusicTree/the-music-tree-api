#!/usr/bin/env python
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL as LIBRARY_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.output.TrackWithoutAlbumAndPlaylistSerializer import (
        TrackWithoutAlbumAndPlaylistSerializer)
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class AlbumDetailedSerializer(serializers.ModelSerializer):
    library_tracks = TrackWithoutAlbumAndPlaylistSerializer(
            source='librarytrack_set', read_only=True, many=True)
    album_artists = ArtistWithOnlyNameSerializer(many=True)
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj) -> float:
        value = LibraryTrack.objects.filter(album=obj).aggregate(
                duration=Sum(ALBUM_ATTRIBUTES_LABEL.DURATION))
        return value[LIBRARY_TRACK_ATTRIBUTES_LABEL.DURATION]

    class Meta:
        model = Album
        fields = [
            ALBUM_ATTRIBUTES_LABEL.UUID,
            ALBUM_ATTRIBUTES_LABEL.NAME,
            ALBUM_ATTRIBUTES_LABEL.YEAR,
            ALBUM_ATTRIBUTES_LABEL.ALBUM_ARTISTS,
            ALBUM_ATTRIBUTES_LABEL.LIBRARY_TRACKS,
            ALBUM_ATTRIBUTES_LABEL.TRACK_COUNT,
            ALBUM_ATTRIBUTES_LABEL.DURATION,
        ]
