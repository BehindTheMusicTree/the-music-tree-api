#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.track.input.schema import \
    LibTrackSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.model.track.LibraryTrack import AttributesLabel
from bodzify_api.serializer.track.input.endpoint.endpoint import LibTrackEndPointSerializer


class FIELDS:
    TRACK_FILE = AttributesLabel.TRACK_FILE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = SAVE_SCHEMA_FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
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
