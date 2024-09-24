#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording, AttributesLabel
from bodzify_api.serializer.musicbrainz.artist.detailed \
    import MusicbrainzArtistDetailedSerializer


class FIELDS:
    UUID = AttributesLabel.UUID
    TITLE = AttributesLabel.TITLE
    SCORE = AttributesLabel.SCORE
    MUSICBRAINZ_ARTISTS = AttributesLabel.MUSICBRAINZ_ARTISTS
    MUSICBRAINZ_LINK = AttributesLabel.MUSICBRAINZ_LINK
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabel.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASE_DATE = AttributesLabel.RELEASE_DATE
    CREATED_ON = AttributesLabel.CREATED_ON
    UPDATED_ON = AttributesLabel.UPDATED_ON


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
