
from rest_framework import serializers

from bodzify_api.serializer.schema.track.input.endpoint.endpoint \
    import LibTrackEndPointSerializer, Fields as EndpointFields
from bodzify_api.validator.mine_track_validators import validate_url


class Fields:
    URL = "url"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = EndpointFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = EndpointFields.TITLE
    ARTISTS_NAMES_STR = EndpointFields.ARTISTS_NAMES
    ALBUM_NAME = EndpointFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STRING = EndpointFields.ALBUM_ARTISTS_NAMES
    POSITION_IN_ALBUM = EndpointFields.POSITION_IN_ALBUM
    GENRE_UUID = EndpointFields.GENRE_UUID
    GENRE_NAME = EndpointFields.GENRE_NAME
    RATING = EndpointFields.RATING
    LANGUAGE = EndpointFields.LANGUAGE


class LibTrackExtractSerializer(LibTrackEndPointSerializer):
    url = serializers.URLField(validators=[validate_url])
