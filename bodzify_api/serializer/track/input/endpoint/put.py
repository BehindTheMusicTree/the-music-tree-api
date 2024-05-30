#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.track.input.schema import \
    LibTrackSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.endpoint.endpoint import LibTrackEndPointSerializer


class FIELDS:
    TRACK_FILE = ATTRIBUTES_LABEL.TRACK_FILE
    SHOULD_CHECK_IF_FINGERPRINT_EXISTS = SAVE_SCHEMA_FIELDS.SHOULD_CHECK_IF_FINGERPRINT_EXISTS
    TITLE = SAVE_SCHEMA_FIELDS.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = SAVE_SCHEMA_FIELDS.GENRE_UUID
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    RATING = SAVE_SCHEMA_FIELDS.RATING
    LANGUAGE = SAVE_SCHEMA_FIELDS.LANGUAGE


class LibTrackPutSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=False)
