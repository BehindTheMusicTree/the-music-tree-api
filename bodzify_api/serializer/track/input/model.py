#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import AttributesLabels, LibraryTrack


class Fields:
    USER = AttributesLabels.USER
    TRACK_FILE = AttributesLabels.TRACK_FILE
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    MUSICBRAINZ_RECORDING = AttributesLabels.MUSICBRAINZ_RECORDING
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR = AttributesLabels.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR
    TITLE = AttributesLabels.TITLE
    ARTISTS = AttributesLabels.ARTISTS
    ALBUM = AttributesLabels.ALBUM
    POSITION_IN_ALBUM = "position_in_album"
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
                  Fields.ARTISTS,
                  Fields.ALBUM,
                  Fields.POSITION_IN_ALBUM,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.ARCHIVED]
