#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabels
from rest_framework import serializers


class Fields:
    USER = AttributesLabels.USER
    TRACK_FILE = AttributesLabels.TRACK_FILE
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    MUSICBRAINZ_RECORDING = AttributesLabels.MUSICBRAINZ_RECORDING
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR = AttributesLabels.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR
    TITLE = AttributesLabels.TITLE
    ARTIST = AttributesLabels.ARTIST
    ALBUM = AttributesLabels.ALBUM
    GENRE = AttributesLabels.GENRE
    RATING = AttributesLabels.RATING
    LANGUAGE = AttributesLabels.LANGUAGE
    ARCHIVED = AttributesLabels.ARCHIVED


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
                  Fields.LANGUAGE,
                  Fields.ARCHIVED]
