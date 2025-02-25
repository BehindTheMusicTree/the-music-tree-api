from bodzify_api.serializer.model.lib_track.input.Fields import \
    Fields as InoutFields


class Fields:
    URL = "url"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = InoutFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = InoutFields.TITLE
    ARTISTS_NAMES_ARRAY = InoutFields.ARTISTS_NAMES_ARRAY
    ALBUM_NAME = InoutFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_ARRAY = InoutFields.ALBUM_ARTISTS_NAMES_ARRAY
    TRACK_NUMBER = InoutFields.TRACK_NUMBER
    GENRE_UUID = InoutFields.GENRE_UUID
    GENRE_NAME = InoutFields.GENRE_NAME
    RATING = InoutFields.RATING
    LANGUAGE = InoutFields.LANGUAGE
