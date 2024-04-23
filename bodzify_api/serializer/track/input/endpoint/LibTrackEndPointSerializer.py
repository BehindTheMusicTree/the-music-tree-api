#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.serializer.track.input.LibTrackSaveSchemaSerializer import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.serializer.album.input.AlbumSaveSchemaSerializer import FIELDS as ALBUM_SAVE_SCHEMA_FIELDS


ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album artists name is."""


class FIELDS:
    USER = SAVE_SCHEMA_FIELDS.USER
    FILE_OBJ = SAVE_SCHEMA_FIELDS.FILE_OBJ
    TITLE = SAVE_SCHEMA_FIELDS.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = ALBUM_SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_STR
    GENRE_UUID = SAVE_SCHEMA_FIELDS.GENRE_UUID
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    RATING = SAVE_SCHEMA_FIELDS.RATING
    LANGUAGE = SAVE_SCHEMA_FIELDS.LANGUAGE
    FORCE_TITLE_GENERATION = "force_title_generation"


class LibTrackEndPointSerializer(InputEndpointSerializer):
    file = serializers.FileField(allow_empty_file=True, allow_null=True, required=False)
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
    genre_uuid = serializers.CharField(
        max_length=22,
        required=False,
        allow_blank=True,
        allow_null=True)
    genre_name = serializers.CharField(
        max_length=settings.CRITERIA_NAME_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    rating = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    language = serializers.CharField(
        max_length=settings.LIB_TRACK_LANGUAGE_LENGTH_MAX,
        required=False,
        allow_blank=True,
        allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)

    class Meta:
        fields = [FIELDS.FILE_OBJ,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STR,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.FORCE_TITLE_GENERATION,]

    def validate(self, data):
        if FIELDS.GENRE_UUID in data and FIELDS.GENRE_NAME in data:
            if data[FIELDS.GENRE_UUID] not in ['', None] and data[FIELDS.GENRE_NAME] not in ['', None]:
                raise serializers.ValidationError("Genre name and genre cannot be specified at the same time.")

        if FIELDS.ALBUM_ARTISTS_NAMES_STR in data:
            if FIELDS.ALBUM_NAME not in data:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
            elif data[FIELDS.ALBUM_NAME] in [None, ""]:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)

        if FIELDS.RATING in data:
            value = data[FIELDS.RATING]
            if value is not None and value != '':
                try:
                    value = int(value)
                except ValueError:
                    raise serializers.ValidationError("Rating must be an integer.")

        return super().validate(data)
