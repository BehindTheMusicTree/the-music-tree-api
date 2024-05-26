#!/usr/bin/env python

import attr
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    TRACK_FILE = ATTRIBUTES_LABEL.TRACK_FILE
    DURATION = ATTRIBUTES_LABEL.DURATION
    MUSICBRAINZ_RECORDING_ID = ATTRIBUTES_LABEL.MUSICBRAINZ_RECORDING_ID
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE


class TrackSaveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.USER,
                  FIELDS.TRACK_FILE,
                  FIELDS.DURATION,
                  FIELDS.MUSICBRAINZ_RECORDING_ID,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
