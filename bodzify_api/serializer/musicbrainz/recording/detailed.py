#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording, ATTRIBUTES_LABEL
from bodzify_api.serializer.musicbrainz.artist.detailed \
    import MusicbrainzArtistDetailedSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    TITLE = ATTRIBUTES_LABEL.TITLE
    SCORE = ATTRIBUTES_LABEL.SCORE
    MUSICBRAINZ_ARTISTS = ATTRIBUTES_LABEL.MUSICBRAINZ_ARTISTS
    MUSICBRAINZ_LINK = ATTRIBUTES_LABEL.MUSICBRAINZ_LINK
    DURATION_IN_SEC = ATTRIBUTES_LABEL.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ATTRIBUTES_LABEL.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASE_DATE = ATTRIBUTES_LABEL.RELEASE_DATE
    CREATED_ON = ATTRIBUTES_LABEL.CREATED_ON
    UPDATED_ON = ATTRIBUTES_LABEL.UPDATED_ON


class MusicbrainzRecordingDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_artists = MusicbrainzArtistDetailedSerializer(many=True)

    class Meta:
        model = MusicbrainzRecording
        fields = [FIELDS.UUID,
                  FIELDS.TITLE,
                  FIELDS.SCORE,
                  FIELDS.MUSICBRAINZ_ARTISTS,
                  FIELDS.MUSICBRAINZ_LINK,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC,
                  FIELDS.RELEASE_DATE,
                  FIELDS.CREATED_ON,
                  FIELDS.UPDATED_ON]
