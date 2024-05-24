#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    FILE_OBJ = ATTRIBUTES_LABEL.FILE_OBJ
    ACOUSTIC_FINGERPRINT = ATTRIBUTES_LABEL.ACOUSTIC_FINGERPRINT
    DURATION = ATTRIBUTES_LABEL.DURATION
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE


class TrackSaveModelSerializer(serializers.ModelSerializer):

    acoustic_fingerprint = serializers.CharField()
    duration = serializers.FloatField()

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.USER,
                  FIELDS.FILE_OBJ,
                  FIELDS.ACOUSTIC_FINGERPRINT,
                  FIELDS.DURATION,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
