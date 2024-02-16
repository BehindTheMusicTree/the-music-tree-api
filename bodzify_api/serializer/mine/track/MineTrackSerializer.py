#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.model.track.MineTrack import MineTrack, ATTRIBUTES_LABEL


class MineTrackSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=settings.MINE_TRACK_TITLE_LENGTH_MAX)
    artist_name = serializers.CharField(max_length=settings.ARTIST_NAME_LENGTH_MAX)
    duration = serializers.IntegerField()
    released_on = serializers.CharField(max_length=settings.MINE_TRACK_RELEASED_ON_LENGTH_MAX)
    url = serializers.CharField(max_length=settings.MINE_TRACK_URL_LENGTH_MAX)

    class Meta:
        fields = [ATTRIBUTES_LABEL.TITLE, 
                  ATTRIBUTES_LABEL.ARTIST_NAME,
                  ATTRIBUTES_LABEL.DURATION,
                  ATTRIBUTES_LABEL.RELEASED_ON,
                  ATTRIBUTES_LABEL.URL]
