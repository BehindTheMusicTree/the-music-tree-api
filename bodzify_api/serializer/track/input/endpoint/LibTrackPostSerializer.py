#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.serializer.track.input.endpoint.LibTrackEndPointSerializer \
    import LibTrackEndPointSerializer, FIELDS as ENDPOINT_FIELDS


class FIELDS:
    FILE_OBJ = ENDPOINT_FIELDS.FILE_OBJ
    SHOULD_CHECK_IF_ACOUSTIC_FINGERPRINT_EXISTS = ENDPOINT_FIELDS.SHOULD_CHECK_IF_ACOUSTIC_FINGERPRINT_EXISTS
    TITLE = ENDPOINT_FIELDS.TITLE
    ARTIST_NAME = ENDPOINT_FIELDS.ARTIST_NAME
    ALBUM_NAME = ENDPOINT_FIELDS.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = ENDPOINT_FIELDS.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = ENDPOINT_FIELDS.GENRE_UUID
    GENRE_NAME = ENDPOINT_FIELDS.GENRE_NAME
    RATING = ENDPOINT_FIELDS.RATING
    LANGUAGE = ENDPOINT_FIELDS.LANGUAGE


class LibTrackPostSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=True)
