#!/usr/bin/env python

import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api import utils
from bodzify_api.serializer.album.output.without_track import AlbumWithoutTracksSerializer
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
    duration_str_in_hour_min_sec_from_duration_in_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> float:
        value = LibraryTrack.objects.filter(artist=obj).aggregate(duration_in_sec=Sum(ATTRIBUTES_LABEL.DURATION_IN_SEC))
        return value[ATTRIBUTES_LABEL.DURATION_IN_SEC]

    def get_duration_str_in_hour_min_sec_from_duration_in_sec(self, obj):
        return str(datetime.timedelta(seconds=obj.duration_in_sec))

    class Meta:
        model = Artist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ALBUMS,
                  ATTRIBUTES_LABEL.LIB_TRACKS,
                  ATTRIBUTES_LABEL.LIB_TRACKS_COUNT,
                  ATTRIBUTES_LABEL.DURATION_IN_SEC]
