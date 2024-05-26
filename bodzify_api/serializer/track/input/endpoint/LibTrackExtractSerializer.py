#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.serializer.track.input.LibTrackSchemaSerializer import \
    LibTrackSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackEndPointSerializer import LibTrackEndPointSerializer
from bodzify_api.validator.mine_track_validators import validate_url


class FIELDS:
    URL = "url"
    SHOULD_CHECK_IF_FINGERPRINT_EXISTS = SAVE_SCHEMA_FIELDS.SHOULD_CHECK_IF_FINGERPRINT_EXISTS
    TITLE = SAVE_SCHEMA_FIELDS.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = SAVE_SCHEMA_FIELDS.GENRE_UUID
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    RATING = SAVE_SCHEMA_FIELDS.RATING
    LANGUAGE = SAVE_SCHEMA_FIELDS.LANGUAGE


class LibTrackExtractSerializer(LibTrackEndPointSerializer):
    url = serializers.URLField(validators=[validate_url])
