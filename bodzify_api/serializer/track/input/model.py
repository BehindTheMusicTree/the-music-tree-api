#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabel
from rest_framework import serializers


class FIELDS:
    USER = AttributesLabel.USER
    TRACK_FILE = AttributesLabel.TRACK_FILE
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    MUSICBRAINZ_RECORDING = AttributesLabel.MUSICBRAINZ_RECORDING
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR = AttributesLabel.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR
    TITLE = AttributesLabel.TITLE
    ARTIST = AttributesLabel.ARTIST
    ALBUM = AttributesLabel.ALBUM
    GENRE = AttributesLabel.GENRE
    RATING = AttributesLabel.RATING
    LANGUAGE = AttributesLabel.LANGUAGE


class TrackModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.USER,
                  FIELDS.TRACK_FILE,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.MUSICBRAINZ_RECORDING,
                  FIELDS.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
