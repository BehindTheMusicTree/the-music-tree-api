#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.track.input.schema import \
    LibTrackSchemaSerializer, Fields as SaveSchemaFields
from bodzify_api.model.track.LibraryTrack import AttributesLabel
from bodzify_api.serializer.track.input.endpoint.endpoint import LibTrackEndPointSerializer


class Fields:
    TRACK_FILE = AttributesLabel.TRACK_FILE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
    TITLE = SaveSchemaFields.TITLE
    ARTIST_NAME = SaveSchemaFields.ARTIST_NAME
    ALBUM_NAME = SaveSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = SaveSchemaFields.GENRE_UUID
    GENRE_NAME = SaveSchemaFields.GENRE_NAME
    RATING = SaveSchemaFields.RATING
    LANGUAGE = SaveSchemaFields.LANGUAGE


class LibTrackPutSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=False)
