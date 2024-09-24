#!/usr/bin/env python

import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.serializer.album.without_track import AlbumWithoutTracksSerializer
from bodzify_api.model.Artist import Artist, AttributesLabel
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class FIELDS:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    ALBUMS = AttributesLabel.ALBUMS
    LIB_TRACKS = AttributesLabel.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabel.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabel.DURATION_STR_IN_HOUR_MIN_SEC


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=AttributesLabel.LIB_TRACKS + '.count')
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> int:
        value = LibraryTrack.objects.filter(artist=obj).aggregate(duration_in_sec=Sum(AttributesLabel.DURATION_IN_SEC))
        return value[AttributesLabel.DURATION_IN_SEC]

    def get_duration_str_in_hour_min_sec(self, obj) -> str:
        return str(datetime.timedelta(seconds=self.get_duration_in_sec(obj)))

    class Meta:
        model = Artist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ALBUMS,
                  FIELDS.LIB_TRACKS,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC]
