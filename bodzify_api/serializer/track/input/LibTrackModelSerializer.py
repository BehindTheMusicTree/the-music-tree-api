#!/usr/bin/env python

import attr
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    FILE_OBJ = ATTRIBUTES_LABEL.FILE_OBJ
    ACOUSTIC_FINGERPRINT = ATTRIBUTES_LABEL.ACOUSTIC_FINGERPRINT
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
                  FIELDS.FILE_OBJ,
                  FIELDS.ACOUSTIC_FINGERPRINT,
                  FIELDS.DURATION,
                  FIELDS.MUSICBRAINZ_RECORDING_ID,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]

    def validate(self, attrs):
        if FIELDS.ACOUSTIC_FINGERPRINT in attrs:
            acoustic_fingerprint = attrs[FIELDS.ACOUSTIC_FINGERPRINT]
            if LibraryTrack.objects.filter(acoustic_fingerprint=acoustic_fingerprint).exists():
                raise serializers.ValidationError("Track with this acoustic fingerprint already exists")

        return super().validate(attrs)
