
from rest_framework import serializers
from bodzify_api.serializer.PutSerializer import PutSerializer
from .endpoint import LibTrackEndPointSerializer, Fields as EndpointFields


class Fields:
    TRACK_FILE = EndpointFields.TRACK_FILE_PUBLIC
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = EndpointFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = EndpointFields.TITLE
    ARTISTS_NAMES_ = EndpointFields.ALBUM_ARTISTS_NAMES_ARRAY
    ALBUM_NAME = EndpointFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_ARRAY = EndpointFields.ALBUM_ARTISTS_NAMES_ARRAY
    POSITION_IN_ALBUM = EndpointFields.POSITION_IN_ALBUM
    GENRE_UUID = EndpointFields.GENRE_UUID
    GENRE_NAME = EndpointFields.GENRE_NAME
    RATING = EndpointFields.RATING
    LANGUAGE = EndpointFields.LANGUAGE
    ARCHIVED = EndpointFields.ARCHIVED


class LibTrackPutSerializer(PutSerializer, LibTrackEndPointSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)
