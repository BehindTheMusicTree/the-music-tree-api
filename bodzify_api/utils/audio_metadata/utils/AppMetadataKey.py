
from enum import Enum

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.serializer.model.lib_track.input.schema.Fields import Fields as LibTrackSchemaFields

APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
    LibTrackSchemaFields.TITLE: str,
    LibTrackSchemaFields.ARTISTS_NAMES: list[str],
    LibTrackSchemaFields.ALBUM_NAME: str,
    LibTrackSchemaFields.ALBUM_ARTISTS_NAMES: list[str],
    LibTrackSchemaFields.GENRE_NAME: str,
    LibTrackSchemaFields.RATING: int,
    LibTrackSchemaFields.LANGUAGE: str,
}


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

    def may_contain_separated_values(self) -> bool:
        result = self in (AppMetadataKey.ARTISTS_NAMES, AppMetadataKey.ALBUM_ARTISTS_NAMES)
        if result and self.get_optional_type() != list[str]:
            raise ImproperlyConfigured(f'Optional type for {self} is not list')
        return result

    def get_optional_type(self) -> type:
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ImproperlyConfigured(f'No optional type defined for {self}')
        return type
