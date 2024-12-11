from rest_framework import serializers

from bodzify_api.serializer.schema.model.lib_track.input.endpoint import LibTrackEndPointSerializer
from bodzify_api.serializer.schema.model.lib_track.input.endpoint import Fields as EndpointFields


class Fields:
    TRACK_FILE_USER_FRIENDLY = EndpointFields.TRACK_FILE_USER_FRIENDLY
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = EndpointFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = EndpointFields.TITLE
    FORCE_TITLE_GENERATION = EndpointFields.FORCE_TITLE_GENERATION
    ARTISTS_NAMES = EndpointFields.ARTISTS_NAMES
    ALBUM_NAME = EndpointFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES = EndpointFields.ALBUM_ARTISTS_NAMES
    POSITION_IN_ALBUM = EndpointFields.POSITION_IN_ALBUM
    GENRE_UUID = EndpointFields.GENRE_UUID
    GENRE_NAME = EndpointFields.GENRE_NAME
    RATING = EndpointFields.RATING
    LANGUAGE = EndpointFields.LANGUAGE


class LibTrackPostSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=True)
