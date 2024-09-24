#!/usr/bin/env python

import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.utils import utils
from bodzify_api.model.Album import Album, AttributesLabel
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    YEAR = AttributesLabel.YEAR
    LIB_TRACKS_COUNT = AttributesLabel.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabel.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumWithoutTrackAndArtistsSerializer(serializers.ModelSerializer):
    track_count = serializers.IntegerField(source=AttributesLabel.LIB_TRACKS + ".count")
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> int:
        value = LibraryTrack.objects.filter(album=obj).aggregate(duration_in_sec=Sum(AttributesLabel.DURATION_IN_SEC))
        return value[AttributesLabel.DURATION_IN_SEC]

    def get_duration_str_in_hour_min_sec(self, obj) -> str:
        return str(datetime.timedelta(seconds=self.get_duration_in_sec(obj)))

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_IN_SEC,]
