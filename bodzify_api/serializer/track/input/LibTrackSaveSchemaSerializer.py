#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.track.input.LibTrackSaveModelSerializer import FIELDS as SAVE_MODEL_FIELDS
from bodzify_api.serializer.album.input.AlbumSaveModelSerializer import FIELDS as ALBUM_SAVE_MODEL_FIELDS


class FIELDS:
    USER = SAVE_MODEL_FIELDS.USER
    FILE = SAVE_MODEL_FIELDS.FILE
    TITLE = SAVE_MODEL_FIELDS.TITLE
    ARTIST_NAME = SAVE_MODEL_FIELDS.ARTIST + "_name"
    ALBUM_NAME = SAVE_MODEL_FIELDS.ALBUM + "_name"
    ALBUM_ARTISTS_NAMES_STR = ALBUM_SAVE_MODEL_FIELDS.ALBUM_ARTISTS + "_names_string"
    GENRE_UUID = SAVE_MODEL_FIELDS.GENRE + "_uuid"
    GENRE_NAME = SAVE_MODEL_FIELDS.GENRE + "_name"
    RATING = SAVE_MODEL_FIELDS.RATING
    LANGUAGE = SAVE_MODEL_FIELDS.LANGUAGE
    FORCE_TITLE_GENERATION = "force_title_generation"


class LibTrackSaveSchemaSerializer(serializers.Serializer):
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
        fields = [FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STR,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.FORCE_TITLE_GENERATION,]

    def validate(self, data):
        if FIELDS.RATING in data:
            value = data[FIELDS.RATING]
            if value is not None and value != '':
                try:
                    value = int(value)
                except ValueError:
                    raise serializers.ValidationError("Rating must be an integer.")

        if FIELDS.GENRE_UUID in data and data[FIELDS.GENRE_UUID] not in ['', None] and not Criteria.objects.filter(
                uuid=data[FIELDS.GENRE_UUID],
                user=self.context['request'].user).exists():
            raise serializers.ValidationError("The genre UUID does not exist.")

        return super().validate(data)
