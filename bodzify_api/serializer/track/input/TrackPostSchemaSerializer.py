#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from upload_validator import FileTypeValidator
from bodzify_api import settings
from bodzify_api.serializer.track.input.TrackSaveSchemaSerializer import TrackSaveSchemaSerializer
from bodzify_api.validator.LibraryTrackSizeValidator import validateTrackSize


class TrackPostSchemaSerializer(TrackSaveSchemaSerializer):

    file = serializers.FileField(
        help_text="Only audio formats accepted.",
        validators=[
            FileExtensionValidator(['flac', 'wav', 'mp3']),
            FileTypeValidator(allowed_types=['audio/*']),
            validateTrackSize],
        required=True)
    title = serializers.CharField(
        max_length=settings.TRACK_TITLE_MAX_CHAR, required=False)
    artistName = serializers.CharField(
        max_length=settings.ARTIST_NAME_MAX_CHAR, required=False, allow_blank=True)
    albumName = serializers.CharField(
        max_length=settings.ALBUM_NAME_MAX_CHAR, required=False, allow_blank=True)
    albumArtistsName = serializers.CharField(
        max_length=settings.ALBUM_ARTISTS_FIELD_MAX_CHAR, required=False, allow_blank=True)
    genreName = serializers.CharField(
        max_length=settings.CRITERIA_NAME_MAX_CHAR, required=False, allow_blank=True)
    rating = serializers.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(settings.TRACK_RATING_MAX_VALUE)],
        required=False,
        allow_null=True)
    language = serializers.CharField(
        max_length=settings.TRACK_LANGUAGE_MAX_CHAR, 
        required=False, 
        allow_blank=True, 
        allow_null=True)
