
from abc import abstractmethod
from typing import TypeVar, cast

from mutagen._file import FileType

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils.AudioFile import AudioFile

from ..exceptions import UnsupportedMetadataError
from ..utils.AppMetadataKey import AppMetadataKey
from ..utils.types import AppMetadataDict, AppMetadataValue, RawMetadataDict, RawMetadataKey


METADATA_ARTISTS_SEPARATION_CHAR = ","


T = TypeVar('T', str, int)


class MetadataManager:

    audio_file: AudioFile
    metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None]
    metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None] | None
    file_raw_metadata: FileType
    raw_metadata_dict: RawMetadataDict

    def __init__(self, audio_file: AudioFile,
                 metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None],
                 metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None] | None = None):
        self.audio_file = audio_file
        self.metadata_keys_direct_map_read = metadata_keys_direct_map_read
        self.metadata_keys_direct_map_write = metadata_keys_direct_map_write
        self.file_raw_metadata = self._extract_raw_metadata()
        self.raw_metadata_dict = self._convert_raw_metadata_to_dict()
        self._regroup_raw_metadata_dict_multiple_entries_in_list()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value(self, app_netadata_key: AppMetadataKey) -> AppMetadataValue:
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

    @abstractmethod
    def _update_formatted_value_in_raw_metadata(
            self, raw_metadata_key: RawMetadataKey, app_metadata_value: AppMetadataValue):
        raise NotImplementedError()

    def _regroup_raw_metadata_dict_multiple_entries_in_list(self):
        raw_metadata_dict_with_regrouped_lists = {}
        for raw_metadata_key, raw_metadata_value in self.raw_metadata_dict.items():
            if isinstance(raw_metadata_value, list):
                raw_metadata_dict_with_regrouped_lists[raw_metadata_key] = raw_metadata_value
            else:
                raw_metadata_dict_with_regrouped_lists[raw_metadata_key] = [raw_metadata_value]
        self.raw_metadata_dict = raw_metadata_dict_with_regrouped_lists

    def get_app_metadata_dict(self) -> AppMetadataDict:
        app_metadata_dict = {}
        for metadata_key in self.metadata_keys_direct_map_read:
            app_metadata_dict[metadata_key] = self.get_app_specific_metadata(metadata_key)
        return app_metadata_dict

    def get_app_specific_metadata(self, app_metadata_key: AppMetadataKey) -> AppMetadataValue:
        if app_metadata_key not in self.metadata_keys_direct_map_read:
            raise UnsupportedMetadataError(f'{app_metadata_key} metadata not supported by this format')

        raw_metadata_key = self.metadata_keys_direct_map_read[app_metadata_key]
        if not raw_metadata_key:
            return self._get_undirectly_mapped_metadata_value(app_metadata_key)

        value = self.raw_metadata_dict.get(raw_metadata_key)

        if not value or not len(value) or not value[0]:
            return None

        app_metadata_key_optional_type = app_metadata_key.get_optional_type()
        if app_metadata_key_optional_type == int:
            return int(value[0]) if value else None
        if app_metadata_key_optional_type == float:
            return float(value[0]) if value else None
        if app_metadata_key_optional_type == str:
            return str(value[0]) if value else None
        if app_metadata_key_optional_type == list[str]:
            if not value:
                return None
            values_list_str = cast(list[str], value)
            if app_metadata_key.may_contain_separated_values():
                values_list_str_with_separated_values_processed: list[str] = []
                for str_with_eventual_separated_values in values_list_str:
                    separated_values = str_with_eventual_separated_values.split(METADATA_ARTISTS_SEPARATION_CHAR)
                    values_list_str_with_separated_values_processed.extend(separated_values)
                return values_list_str_with_separated_values_processed
            return values_list_str
        raise ImproperlyConfigured(f'Unsupported metadata type: {app_metadata_key_optional_type}')

    def update_bulk(self, app_metadata_dict: AppMetadataDict):
        if not self.metadata_keys_direct_map_write:
            raise UnsupportedMetadataError('This format does not support metadata modification')

        for app_metadata_key in list(app_metadata_dict.keys()):
            value = app_metadata_dict[app_metadata_key]
            if app_metadata_key not in self.metadata_keys_direct_map_write:
                raise UnsupportedMetadataError(f'{app_metadata_key} metadata not supported by this format')
            else:
                raw_metadata_key = self.metadata_keys_direct_map_write[app_metadata_key]
                if raw_metadata_key:
                    self._update_formatted_value_in_raw_metadata(
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
