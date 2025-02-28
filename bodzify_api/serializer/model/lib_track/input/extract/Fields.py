from bodzify_api.serializer.model.lib_track.input.Fields import Fields as InputFields


class Fields:
    URL = "url"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = InputFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = InputFields.TITLE
    ARTISTS_NAMES_ARRAY = InputFields.ARTISTS_NAMES_ARRAY
    ALBUM_NAME = InputFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_ARRAY = InputFields.ALBUM_ARTISTS_NAMES_ARRAY
    TRACK_NUMBER = InputFields.TRACK_NUMBER
    GENRE = InputFields.GENRE
    RATING = InputFields.RATING
    LANGUAGE = InputFields.LANGUAGE
