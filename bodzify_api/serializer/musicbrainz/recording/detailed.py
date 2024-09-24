#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording, AttributesLabel
from bodzify_api.serializer.musicbrainz.artist.detailed \
    import MusicbrainzArtistDetailedSerializer


class Fields:
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
