#!/usr/bin/env python

import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.serializer.album.without_track import AlbumWithoutTracksSerializer
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    ALBUMS = ATTRIBUTES_LABEL.ALBUMS
    LIB_TRACKS = ATTRIBUTES_LABEL.LIB_TRACKS
    LIB_TRACKS_COUNT = ATTRIBUTES_LABEL.LIB_TRACKS_COUNT
    DURATION_IN_SEC = ATTRIBUTES_LABEL.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ATTRIBUTES_LABEL.DURATION_STR_IN_HOUR_MIN_SEC


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=ATTRIBUTES_LABEL.LIB_TRACKS + '.count')
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> int:
        value = LibraryTrack.objects.filter(artist=obj).aggregate(duration_in_sec=Sum(ATTRIBUTES_LABEL.DURATION_IN_SEC))
        return value[ATTRIBUTES_LABEL.DURATION_IN_SEC]

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
