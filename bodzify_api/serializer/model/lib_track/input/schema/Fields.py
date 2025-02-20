from bodzify_api.serializer.model.lib_track.input.Fields import Fields as EndpointFields


class Fields:
    TRACK_FILE_PUBLIC = EndpointFields.TRACK_FILE_PUBLIC
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
