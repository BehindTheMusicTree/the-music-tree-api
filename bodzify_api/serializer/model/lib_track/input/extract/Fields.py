from bodzify_api.serializer.model.lib_track.input.Fields import Fields as EndpointFields


class Fields:
    URL = "url"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = EndpointFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = EndpointFields.TITLE
    ARTISTS_NAMES_ARRAY = EndpointFields.ARTISTS_NAMES_ARRAY
    ALBUM_NAME = EndpointFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_ARRAY = EndpointFields.ALBUM_ARTISTS_NAMES_ARRAY
    POSITION_IN_ALBUM = EndpointFields.POSITION_IN_ALBUM
    GENRE_UUID = EndpointFields.GENRE_UUID
    GENRE_NAME = EndpointFields.GENRE_NAME
    RATING = EndpointFields.RATING
    LANGUAGE = EndpointFields.LANGUAGE
