#!/usr/bin/env python

import datetime
from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording, ATTRIBUTES_LABEL
from bodzify_api.serializer.musicbrainz.artist.detailed \
    import MusicbrainzArtistDetailedSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    TITLE = ATTRIBUTES_LABEL.TITLE
    MUSICBRAINZ_ARTISTS = ATTRIBUTES_LABEL.MUSICBRAINZ_ARTISTS
    MUSICBRAINZ_LINK = ATTRIBUTES_LABEL.MUSICBRAINZ_LINK
    DURATION_IN_SEC = ATTRIBUTES_LABEL.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ATTRIBUTES_LABEL.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASE_DATE = ATTRIBUTES_LABEL.RELEASE_DATE
    CREATED_ON = ATTRIBUTES_LABEL.CREATED_ON
    UPDATED_ON = ATTRIBUTES_LABEL.UPDATED_ON


class MusicbrainzRecordingDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_artists = MusicbrainzArtistDetailedSerializer(many=True)
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_str_in_hour_min_sec(self, obj):
        return str(datetime.timedelta(seconds=obj.duration_in_sec))

    class Meta:
        model = MusicbrainzRecording
        fields = [FIELDS.UUID,
                  FIELDS.TITLE,
                  FIELDS.MUSICBRAINZ_ARTISTS,
                  FIELDS.MUSICBRAINZ_LINK,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC,
                  FIELDS.RELEASE_DATE,
                  FIELDS.CREATED_ON,
                  FIELDS.UPDATED_ON]
