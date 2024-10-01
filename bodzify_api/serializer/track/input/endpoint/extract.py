#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.input.schema import Fields as SaveSchemaFields
from bodzify_api.serializer.track.input.endpoint.endpoint import LibTrackEndPointSerializer
from bodzify_api.validator.mine_track_validators import validate_url


class Fields:
    URL = "url"
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
    TITLE = SaveSchemaFields.TITLE
    ARTIST_NAME = SaveSchemaFields.ARTIST_NAME
    ALBUM_NAME = SaveSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR
    GENRE_UUID = SaveSchemaFields.GENRE_UUID
    GENRE_NAME = SaveSchemaFields.GENRE_NAME
    RATING = SaveSchemaFields.RATING
    LANGUAGE = SaveSchemaFields.LANGUAGE


class LibTrackExtractSerializer(LibTrackEndPointSerializer):
    url = serializers.URLField(validators=[validate_url])
