#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.serializer.track.input.endpoint.endpoint \
    import LibTrackEndPointSerializer, Fields as EndpointFields


class Fields:
    TRACK_FILE = EndpointFields.TRACK_FILE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = EndpointFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
    TITLE = EndpointFields.TITLE
    ARTIST_NAME = EndpointFields.ARTIST_NAME
    ALBUM_NAME = EndpointFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = EndpointFields.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = EndpointFields.GENRE_UUID
    GENRE_NAME = EndpointFields.GENRE_NAME
    RATING = EndpointFields.RATING
    LANGUAGE = EndpointFields.LANGUAGE


class LibTrackPostSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=True)
