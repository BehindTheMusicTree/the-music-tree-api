#!/usr/bin/env python
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class AlbumWithoutTrackAndArtistsSerializer(serializers.ModelSerializer):
    track_count = serializers.IntegerField(source='library_tracks.count')
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
            ALBUM_ATTRIBUTES_LABEL.LIB_TRACKS_COUNT,
            ALBUM_ATTRIBUTES_LABEL.DURATION,
        ]
