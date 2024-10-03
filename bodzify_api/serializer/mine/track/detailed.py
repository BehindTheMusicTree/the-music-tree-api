#!/usr/bin/env python

import datetime
from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.model.track.MineTrack import AttributesLabels


class Fields:
    TITLE = AttributesLabels.TITLE
    ARTIST_NAME = AttributesLabels.ARTIST_NAME
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASED_ON = AttributesLabels.RELEASED_ON
    URL = AttributesLabels.URL


class MineTrackSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=settings.MINE_TRACK_TITLE_LEN_MAX)
    artist_name = serializers.CharField(max_length=settings.ARTIST_NAME_LEN_MAX)
    duration_in_sec = serializers.IntegerField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()
    released_on = serializers.CharField(max_length=settings.MINE_TRACK_RELEASED_ON_LEN_MAX)
    url = serializers.CharField(max_length=settings.MINE_TRACK_URL_LEN_MAX)

    class Meta:
        fields = [Fields.TITLE,
                  Fields.ARTIST_NAME,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.RELEASED_ON,
                  Fields.URL]

    def get_duration_str_in_hour_min_sec(self, obj) -> str:
        return str(datetime.timedelta(seconds=obj.duration_in_sec))
