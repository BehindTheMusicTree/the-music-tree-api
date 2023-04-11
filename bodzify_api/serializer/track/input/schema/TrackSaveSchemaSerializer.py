#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from bodzify_api import settings
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL

ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be 
        specified if album artists name is."""


class ATTRIBUTES_LABEL:
    ARTIST_NAME = "artistName"
    ALBUM_NAME = "albumName"
    ALBUM_ARTISTS_NAME_STRING = "albumArtistsNameString"
    GENRE_NAME = "genreName"


class TrackSaveSchemaSerializer(InputSerializer):

    title = serializers.CharField(
        max_length=settings.TRACK_TITLE_MAX_CHAR, 
        required=False, 
        allow_null=True)
    artistName = serializers.CharField(
        max_length=settings.ARTIST_NAME_MAX_CHAR, 
        required=False, 
        allow_blank=True, 
        allow_null=True)
    albumName = serializers.CharField(
        max_length=settings.ALBUM_NAME_MAX_CHAR, 
        required=False, 
        allow_blank=True, 
        allow_null=True)
    albumArtistsNameString = serializers.CharField(
        max_length=settings.ALBUM_ARTISTS_FIELD_MAX_CHAR,
        required=False, 
        allow_blank=True, 
        allow_null=True)
    genreName = serializers.CharField(
        max_length=settings.CRITERIA_NAME_MAX_CHAR, 
        required=False, 
        allow_blank=True, 
        allow_null=True)
    rating = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(settings.TRACK_RATING_MAX_VALUE)],
        required=False,
        allow_null=True)
    language = serializers.CharField(
        max_length=settings.TRACK_LANGUAGE_MAX_CHAR,
        required=False,
        allow_blank=True,
        allow_null=True)

    class Meta:
        fields = [TRACK_ATTRIBUTES_LABEL.TITLE,
                  ATTRIBUTES_LABEL.ARTIST_NAME,
                  ATTRIBUTES_LABEL.ALBUM_NAME,
                  ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING,
                  ATTRIBUTES_LABEL.GENRE_NAME,
                  TRACK_ATTRIBUTES_LABEL.RATING]

    def validate(self, data):
        if ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING in data:
            if ATTRIBUTES_LABEL.ALBUM_NAME not in data:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
            elif data[ATTRIBUTES_LABEL.ALBUM_NAME] in [None, ""]:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
        return super().validate(data)
