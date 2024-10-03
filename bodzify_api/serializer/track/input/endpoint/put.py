#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.input.schema import Fields as SaveSchemaFields
from bodzify_api.model.track.LibraryTrack import AttributesLabels
from bodzify_api.serializer.track.input.endpoint.endpoint import LibTrackEndPointSerializer


class Fields:
    TRACK_FILE = AttributesLabels.TRACK_FILE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
    TITLE = SaveSchemaFields.TITLE
    ARTIST_NAME = SaveSchemaFields.ARTIST_NAME
    ALBUM_NAME = SaveSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = SaveSchemaFields.GENRE_UUID
    GENRE_NAME = SaveSchemaFields.GENRE_NAME
    RATING = SaveSchemaFields.RATING
    LANGUAGE = SaveSchemaFields.LANGUAGE
    ARCHIVED = SaveSchemaFields.ARCHIVED


class LibTrackPutSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)
