
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from bodzify_api.utils.audio_metadata.utils.types import RawMetadataKey


class Id3v1RawMetadataKey(RawMetadataKey):
    TITLE = AppMetadataKey.TITLE.value
    ARTISTS_NAMES_STR = AppMetadataKey.ARTISTS_NAMES_STR.value
    ALBUM_NAME = AppMetadataKey.ALBUM_NAME.value
    GENRE_CODE = 'genre_code'
    YEAR = 'year'
    TRACK_NUMBER = 'track_number'
    COMMENT = 'comment'
