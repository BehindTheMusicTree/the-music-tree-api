#!/usr/bin/env python
import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.utils import utils
from bodzify_api.model.Album import Album, AttributesLabel as AttributesLabel
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer


class FIELDS:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    YEAR = AttributesLabel.YEAR
    ALBUM_ARTISTS = AttributesLabel.ALBUM_ARTISTS
    LIB_TRACKS_COUNT = AttributesLabel.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabel.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumWithoutTracksSerializer(serializers.ModelSerializer):
    album_artists = ArtistWithOnlyNameSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=AttributesLabel.LIB_TRACKS + '.count')
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> int:
        value = LibraryTrack.objects.filter(album=obj).aggregate(duration_in_sec=Sum(AttributesLabel.DURATION_IN_SEC))
        return value[AttributesLabel.DURATION_IN_SEC]

    def get_duration_str_in_hour_min_sec(self, obj) -> str:
        return str(datetime.timedelta(seconds=self.get_duration_in_sec(obj)))

    class Meta:
        model = Album
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.YEAR,
                  FIELDS.ALBUM_ARTISTS,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC]
