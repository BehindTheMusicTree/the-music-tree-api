#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.input.schema.LibTrackSaveSchemaSerializer import \
    LibTrackSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.validator.MineTrackUrlValidator import validate_url


class FIELDS:
    URL = "url"
    TITLE = SAVE_SCHEMA_FIELDS.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STRING
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    RATING = SAVE_SCHEMA_FIELDS.RATING
    LANGUAGE = SAVE_SCHEMA_FIELDS.LANGUAGE


class LibTrackExtractSchemaSerializer(LibTrackSaveSchemaSerializer):
    url = serializers.URLField(validators=[validate_url])

    class Meta(LibTrackSaveSchemaSerializer.Meta):
        fields = [FIELDS.URL,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
