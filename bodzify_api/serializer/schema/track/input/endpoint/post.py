
from rest_framework import serializers

from bodzify_api.serializer.schema.track.input.endpoint.endpoint \
    import Fields as EndpointFields, LibTrackEndPointSerializer


class Fields:
    FILE = EndpointFields.FILE
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = EndpointFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = EndpointFields.TITLE
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
