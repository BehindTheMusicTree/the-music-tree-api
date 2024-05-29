#!/usr/bin/env python

import datetime
from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.model.track.MineTrack import ATTRIBUTES_LABEL


class FIELDS:
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST_NAME = ATTRIBUTES_LABEL.ARTIST_NAME
    DURATION = ATTRIBUTES_LABEL.DURATION
    DURATION_STR = ATTRIBUTES_LABEL.DURATION + "_str"
    RELEASED_ON = ATTRIBUTES_LABEL.RELEASED_ON
    URL = ATTRIBUTES_LABEL.URL


class MineTrackSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=settings.MINE_TRACK_TITLE_LEN_MAX)
    artist_name = serializers.CharField(max_length=settings.ARTIST_NAME_LEN_MAX)
    duration = serializers.IntegerField()
    duration_str = serializers.SerializerMethodField()
    released_on = serializers.CharField(max_length=settings.MINE_TRACK_RELEASED_ON_LEN_MAX)
    url = serializers.CharField(max_length=settings.MINE_TRACK_URL_LEN_MAX)

    class Meta:
        fields = [FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.DURATION,
                  FIELDS.DURATION_STR,
                  FIELDS.RELEASED_ON,
                  FIELDS.URL]

    def get_duration_str(self, obj):
        duration = datetime.timedelta(seconds=obj.duration)
        return str(duration)
