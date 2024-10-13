#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.LibraryTrack import AttributesLabels
from bodzify_api.serializer.track.input.endpoint.endpoint import LibTrackEndPointSerializer, Fields as EndpointFields


class Fields:
    TRACK_FILE = AttributesLabels.TRACK_FILE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = EndpointFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
    TITLE = EndpointFields.TITLE
    ARTISTS_NAMES_STR = EndpointFields.ARTISTS_NAMES_STR
    ALBUM_NAME = EndpointFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = EndpointFields.ALBUM_ARTISTS_NAMES_STR
    POSITION_IN_ALBUM = EndpointFields.POSITION_IN_ALBUM
    GENRE_UUID = EndpointFields.GENRE_UUID
    GENRE_NAME = EndpointFields.GENRE_NAME
    RATING = EndpointFields.RATING
    LANGUAGE = EndpointFields.LANGUAGE
    ARCHIVED = EndpointFields.ARCHIVED


class LibTrackPutSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)
