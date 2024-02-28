#!/usr/bin/env python

from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from bodzify_api import settings
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.serializer.track.input.LibTrackSaveModelSerializer import FIELDS as SAVE_MODEL_FIELDS
from bodzify_api.serializer.album.input.AlbumSaveModelSerializer import FIELDS as ALBUM_SAVE_MODEL_FIELDS


ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album artists name is."""


class FIELDS:
    FILE = SAVE_MODEL_FIELDS.FILE
    TITLE = SAVE_MODEL_FIELDS.TITLE
    ARTIST_NAME = SAVE_MODEL_FIELDS.ARTIST + "_name"
    ALBUM_NAME = SAVE_MODEL_FIELDS.ALBUM + "_name"
    ALBUM_ARTISTS_NAMES_STRING = ALBUM_SAVE_MODEL_FIELDS.ALBUM_ARTISTS + "_names_string"
    GENRE_NAME = SAVE_MODEL_FIELDS.GENRE + "_name"
    RATING = SAVE_MODEL_FIELDS.RATING
    LANGUAGE = SAVE_MODEL_FIELDS.LANGUAGE
    FORCE_TITLE_GENERATION = "force_title_generation"


class LibTrackSaveSchemaSerializer(InputSerializer):
    file = serializers.FileField(
        allow_empty_file=True,
        allow_null=True,
        required=False)
    title = serializers.CharField(
        max_length=settings.LIB_TRACK_TITLE_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    artist_name = serializers.CharField(
        max_length=settings.ARTIST_NAME_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    album_name = serializers.CharField(
        max_length=settings.ALBUM_NAME_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    album_artists_names_string = serializers.CharField(
        max_length=settings.ALBUM_ARTISTS_FIELD_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    genre_name = serializers.CharField(
        max_length=settings.CRITERIA_NAME_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    rating = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(settings.LIB_TRACK_RATING_VALUE_MAX)],
        required=False,
        allow_null=True)
    language = serializers.CharField(
        max_length=settings.LIB_TRACK_LANGUAGE_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)

    class Meta:
        fields = [FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.FORCE_TITLE_GENERATION,]

    def validate(self, data):
        if FIELDS.ALBUM_ARTISTS_NAMES_STRING in data:
            if FIELDS.ALBUM_NAME not in data:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
            elif data[FIELDS.ALBUM_NAME] in [None, ""]:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
        return super().validate(data)
