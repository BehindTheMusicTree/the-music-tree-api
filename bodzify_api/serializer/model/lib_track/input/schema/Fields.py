from bodzify_api.serializer.model.lib_track.input.Fields import     Fields as InoutFields


class Fields:
    TRACK_FILE_PUBLIC = InoutFields.TRACK_FILE_PUBLIC
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = InoutFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = InoutFields.TITLE
    FORCE_TITLE_GENERATION = InoutFields.FORCE_TITLE_GENERATION
    ARTISTS_NAMES = InoutFields.ARTISTS_NAMES
    ALBUM_NAME = InoutFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES = InoutFields.ALBUM_ARTISTS_NAMES
    TRACK_NUMBER = InoutFields.TRACK_NUMBER
    GENRE_UUID = InoutFields.GENRE_UUID
    GENRE_NAME = InoutFields.GENRE_NAME
    RATING = InoutFields.RATING
    LANGUAGE = InoutFields.LANGUAGE
