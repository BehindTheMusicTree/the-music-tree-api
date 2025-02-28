
from enum import Enum

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.serializer.model.lib_track.input.schema.Fields import Fields as LibTrackSchemaFields
from bodzify_api.serializer.model.criteria.input.Fields import Fields as CriteriaSchemaFields


class AppMetadataKey(str, Enum):
    TITLE = LibTrackSchemaFields.TITLE
    ARTISTS_NAMES = LibTrackSchemaFields.ARTISTS_NAMES
    ALBUM_NAME = LibTrackSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES = LibTrackSchemaFields.ALBUM_ARTISTS_NAMES
    GENRE_NAME = f'{LibTrackSchemaFields.GENRE}_{CriteriaSchemaFields.NAME_PUBLIC}'
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
        APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
            AppMetadataKey.TITLE: str,
            AppMetadataKey.ARTISTS_NAMES: list[str],
            AppMetadataKey.ALBUM_NAME: str,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: list[str],
            AppMetadataKey.GENRE_NAME: str,
            AppMetadataKey.RATING: int,
            AppMetadataKey.LANGUAGE: str,
        }
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ImproperlyConfigured(f'No optional type defined for {self}')
        return type
