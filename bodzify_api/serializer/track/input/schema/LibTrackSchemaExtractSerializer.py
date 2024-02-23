#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import \
    LibTrackSchemaSaveSerializer, FIELDS as SCHEMA_SAVE_FIELDS
from bodzify_api.validator.MineTrackUrlValidator import validate_url


class FIELDS:
    URL = "url"
    TITLE = SCHEMA_SAVE_FIELDS.TITLE
    ARTIST_NAME = SCHEMA_SAVE_FIELDS.ARTIST_NAME
    ALBUM_NAME = SCHEMA_SAVE_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = SCHEMA_SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING
    GENRE_NAME = SCHEMA_SAVE_FIELDS.GENRE_NAME
    RATING = SCHEMA_SAVE_FIELDS.RATING
    LANGUAGE = SCHEMA_SAVE_FIELDS.LANGUAGE


class LibTrackSchemaExtractSerializer(LibTrackSchemaSaveSerializer):
    url = serializers.URLField(validators=[validate_url])

    class Meta(LibTrackSchemaSaveSerializer.Meta):
        fields = [FIELDS.URL,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
