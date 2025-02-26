
from abc import abstractmethod
from typing import Type, TypeVar

from django.core.exceptions import ImproperlyConfigured
from mutagen._file import FileType

from bodzify_api.utils import data_transformer
from bodzify_api.utils.AudioFile import AudioFile

from ..exceptions import UnsupportedMetadataError
from ..utils.AppMetadataKey import AppMetadataKey
from ..utils.types import AppMetadataDict, AppMetadataValue, RawMetadataDict, RawMetadataKey, RawMetadataValue


METADATA_ARTISTS_SEPARATION_CHAR = ","

T = TypeVar('T', str, int)


class MetadataManager:

    APP_METADATA_KEY_TYPE_MAP = {
        AppMetadataKey.TITLE: str,
        AppMetadataKey.ARTISTS_NAMES_STR: str,
        AppMetadataKey.ALBUM_NAME: str,
        AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: str,
        AppMetadataKey.GENRE_NAME: str,
        AppMetadataKey.RATING: int,
        AppMetadataKey.LANGUAGE: str,
    }

    audio_file: AudioFile
    metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None]
    metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None]
    file_raw_metadata: FileType
    raw_metadata_dict: dict[RawMetadataKey, RawMetadataValue]

    def __init__(
            self, audio_file: AudioFile,
            metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None],
            metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None]):
        self.audio_file = audio_file
        self.metadata_keys_direct_map_read = metadata_keys_direct_map_read
        self.metadata_keys_direct_map_write = metadata_keys_direct_map_write
        self.file_raw_metadata = self._extract_raw_metadata()
        self.raw_metadata_dict = self._convert_raw_metadata_to_dict()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value(self, app_netadata_key: AppMetadataKey) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    def _extract_raw_metadata(self) -> FileType:
        raise NotImplementedError()

    @abstractmethod
    def _convert_raw_metadata_to_dict(self) -> RawMetadataDict:
        raise NotImplementedError()

    @abstractmethod
    def _update_undirectly_mapped_metadata(
            self, app_metadata_value: AppMetadataValue, app_metadata_key: AppMetadataKey):
        raise NotImplementedError()

    def _get_first_value_in_raw_metadata_dict_or_none(
            self, raw_metadata_key: RawMetadataKey, value_type: Type[T]) -> str | int | None:
        if value_type == str:
            value = data_transformer.get_first_value_str_if_exists_in_str_dict_or_none(
                str_dict=self.raw_metadata_dict, key=raw_metadata_key)
            return value.strip() if value else None
        elif value_type == int:
            return data_transformer.get_first_value_int_if_exists_in_str_dict_or_none(
                str_dict=self.raw_metadata_dict, key=raw_metadata_key)
        else:
            raise ImproperlyConfigured('Value type not handled')

    def _get_value_from_raw_metadata_dict(
            self, raw_metadata_key: RawMetadataKey, value_type: Type[T]) -> AppMetadataValue:
        return self.raw_metadata_dict.get(raw_metadata_key, None)

    def _update_prepared_value_in_raw_metadata(
            self, raw_metadata_key: RawMetadataKey, app_metadata_value: AppMetadataValue):
        self.file_raw_metadata[raw_metadata_key] = app_metadata_value

    def get_app_metadata_dict(self) -> AppMetadataDict:
        app_metadata_dict = {}
        for metadata_key in self.metadata_keys_direct_map_read:
            app_metadata_dict[metadata_key] = self.get_app_specific_metadata(metadata_key)
        return app_metadata_dict

    def get_app_specific_metadata(self, app_metadata_key: AppMetadataKey):
        if app_metadata_key not in self.metadata_keys_direct_map_read:
            raise UnsupportedMetadataError(f'{app_metadata_key} metadata not supported by this format')

        raw_metadata_key = self.metadata_keys_direct_map_read[app_metadata_key]
        if not raw_metadata_key:
            return self._get_undirectly_mapped_metadata_value(app_metadata_key)
        else:
            value_type = self.APP_METADATA_KEY_TYPE_MAP[app_metadata_key]
            return self._get_value_from_raw_metadata_dict(raw_metadata_key=raw_metadata_key, value_type=value_type)

    def update_bulk(self, app_metadata_dict: AppMetadataDict):
        for app_metadata_key in list(app_metadata_dict.keys()):
            value = app_metadata_dict[app_metadata_key]
            if app_metadata_key not in self.metadata_keys_direct_map_write:
                raise UnsupportedMetadataError(f'{app_metadata_key} metadata not supported by this format')
            else:
                raw_metadata_key = self.metadata_keys_direct_map_write[app_metadata_key]
                if raw_metadata_key:
                    self._update_prepared_value_in_raw_metadata(
                        raw_metadata_key=raw_metadata_key, app_metadata_value=value)
                else:
                    self._update_undirectly_mapped_metadata(
                        app_metadata_value=value, app_metadata_key=app_metadata_key)

        self.file_raw_metadata.save(self.audio_file.get_file_path_or_object())

    def delete_metadata(self) -> bool:
        try:
            self.file_raw_metadata.delete()
            return True
        except Exception:
            return False
