#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabel
from rest_framework import serializers


class Fields:
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
        fields = [Fields.USER,
                  Fields.TRACK_FILE,
                  Fields.DURATION_IN_SEC,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR,
                  Fields.TITLE,
                  Fields.ARTIST,
                  Fields.ALBUM,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE]
