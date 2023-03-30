#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from bodzify_api import settings
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.validator.MineTrackUrlValidator import validateUrl


class TrackExtractSchemaSerializer(InputSerializer):
    url = serializers.URLField(validators=[validateUrl])
    title = serializers.CharField(
        max_length=settings.TRACK_TITLE_MAX_CHAR, required=False)
    artistName = serializers.CharField(
        max_length=settings.ARTIST_NAME_MAX_CHAR, required=False)
    albumName = serializers.CharField(
        max_length=settings.ALBUM_NAME_MAX_CHAR, required=False)
    albumArtistsName = serializers.CharField(
        max_length=settings.ALBUM_ARTISTS_FIELD_MAX_CHAR, required=False)
    genreName = serializers.CharField(
        max_length=settings.CRITERIA_NAME_MAX_CHAR, required=False)
    rating = serializers.IntegerField(
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(settings.TRACK_RATING_MAX_VALUE)],
        required=False)
    language = serializers.CharField(
        max_length=settings.TRACK_LANGUAGE_MAX_CHAR, required=False)
