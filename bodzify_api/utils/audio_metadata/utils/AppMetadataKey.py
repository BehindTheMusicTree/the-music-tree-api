
from enum import Enum

from bodzify_api.serializer.model.lib_track.input.schema.Fields import Fields as LibTrackSchemaFields


class AppMetadataKey(str, Enum):
    TITLE = LibTrackSchemaFields.TITLE
    ARTISTS_NAMES = LibTrackSchemaFields.ARTISTS_NAMES
    ALBUM_NAME = LibTrackSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES = LibTrackSchemaFields.ALBUM_ARTISTS_NAMES
    GENRE_NAME = LibTrackSchemaFields.GENRE_NAME
    RATING = LibTrackSchemaFields.RATING
    LANGUAGE = LibTrackSchemaFields.LANGUAGE
    # RELEASE_DATE = 'release_date'
    # TRACK_NUMBER = 'track_number'
    # BPM = 'bpm'
