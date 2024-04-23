#!/usr/bin/env python

from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from bodzify_api import settings
from bodzify_api.serializer.track.input.LibTrackSaveSchemaSerializer import \
    LibTrackSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackEndPointSerializer \
    import LibTrackEndPointSerializer, FIELDS as ENDPOINT_FIELDS
from bodzify_api.validator.track_file_validator \
    import validate_filename_length, validate_size, validate_is_audio, validate_content_type_is_audio


class FIELDS:
    FILE_OBJ = ENDPOINT_FIELDS.FILE_OBJ
    TITLE = SAVE_SCHEMA_FIELDS.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = SAVE_SCHEMA_FIELDS.GENRE_UUID
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    RATING = SAVE_SCHEMA_FIELDS.RATING
    LANGUAGE = SAVE_SCHEMA_FIELDS.LANGUAGE


class LibTrackPostSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(
        help_text="Only audio formats accepted.",
        validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS),
                    validate_filename_length,
                    validate_size,
                    validate_is_audio,
                    validate_content_type_is_audio],
        required=True)  # This is the only difference with LibTrackEndPointSerializer as the file is required for post

    class Meta(LibTrackSaveSchemaSerializer.Meta):
        fields = [FIELDS.FILE_OBJ,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STR,
                  FIELDS.GENRE_UUID,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
