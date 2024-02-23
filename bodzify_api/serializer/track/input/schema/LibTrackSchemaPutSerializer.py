#!/usr/bin/env python

from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from bodzify_api import settings
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import \
    LibTrackSchemaSaveSerializer, FIELDS as SCHEMA_SAVE_FIELDS
from bodzify_api.model.track.LibraryTrack import LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.validator.TrackFileValidator import validate_content_type_is_audio, validate_size


class FIELDS:
    FILE = LIB_TRACK_ATTRIBUTES_LABEL.FILE
    TITLE = SCHEMA_SAVE_FIELDS.TITLE
    ARTIST_NAME = SCHEMA_SAVE_FIELDS.ARTIST_NAME
    ALBUM_NAME = SCHEMA_SAVE_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = SCHEMA_SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING
    GENRE_NAME = SCHEMA_SAVE_FIELDS.GENRE_NAME
    RATING = SCHEMA_SAVE_FIELDS.RATING
    LANGUAGE = SCHEMA_SAVE_FIELDS.LANGUAGE


class LibTrackPutSchemaSerializer(LibTrackSchemaSaveSerializer):

    file = serializers.FileField(
        help_text="Only audio formats accepted.",
        validators=[
            FileExtensionValidator(settings.TRACK_FILE_EXTENSIONS),
            validate_content_type_is_audio,
            validate_size],
        required=False)

    class Meta(LibTrackSchemaSaveSerializer.Meta):
        fields = [FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
