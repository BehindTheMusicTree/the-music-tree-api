#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzRecording import (
    AttributesLabels, MusicbrainzRecording)
from bodzify_api.serializer.musicbrainz.artist.detailed import \
    MusicbrainzArtistDetailedSerializer


class Fields:
    UUID = AttributesLabels.UUID
    TITLE = AttributesLabels.TITLE
    SCORE = AttributesLabels.SCORE
    MUSICBRAINZ_ARTISTS = AttributesLabels.MUSICBRAINZ_ARTISTS
    MUSICBRAINZ_LINK = AttributesLabels.MUSICBRAINZ_LINK
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASE_DATE = AttributesLabels.RELEASE_DATE
    CREATED_ON = AttributesLabels.CREATED_ON
    UPDATED_ON = AttributesLabels.UPDATED_ON


class MusicbrainzRecordingDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_artists = MusicbrainzArtistDetailedSerializer(many=True)

    class Meta:
        model = MusicbrainzRecording
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.SCORE,
                  Fields.MUSICBRAINZ_ARTISTS,
                  Fields.MUSICBRAINZ_LINK,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.RELEASE_DATE,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
