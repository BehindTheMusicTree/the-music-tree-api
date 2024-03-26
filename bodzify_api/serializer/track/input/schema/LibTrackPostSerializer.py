#!/usr/bin/env python

from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from bodzify_api.serializer.track.input.LibTrackSaveModelSerializer import FIELDS as SAVE_MODEL_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackSaveSchemaSerializer import \
    LibTrackSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.validator.TrackFileValidator import validate_content_type_is_audio, validate_size
from bodzify_api import settings


class FIELDS:
    FILE = SAVE_MODEL_FIELDS.FILE
    TITLE = SAVE_SCHEMA_FIELDS.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    RATING = SAVE_SCHEMA_FIELDS.RATING
    LANGUAGE = SAVE_SCHEMA_FIELDS.LANGUAGE


class LibTrackPostSerializer(LibTrackSaveSchemaSerializer):

    file = serializers.FileField(
        help_text="Only audio formats accepted.",
        validators=[
            FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS),
            validate_content_type_is_audio,
            validate_size],
        required=True)

    class Meta(LibTrackSaveSchemaSerializer.Meta):
        fields = [FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
