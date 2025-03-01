
from abc import abstractmethod
from typing import TypeVar, cast

from mutagen._file import FileType as MutagenMetadata

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils.AudioFile import AudioFile

from ..exceptions import MetadataNotSupportedError
from ..utils.AppMetadataKey import AppMetadataKey
from ..utils.types import AppMetadata, AppMetadataValue, RawMetadataDict, RawMetadataKey


METADATA_ARTISTS_SEPARATION_CHAR = ","


T = TypeVar('T', str, int)


class MetadataManager:

    audio_file: AudioFile
    metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None]
    metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None] | None
    raw_mutagen_metadata: MutagenMetadata | None = None
    raw_clean_metadata: RawMetadataDict | None = None
    update_using_mutagen_metadata: bool

    def __init__(self, audio_file: AudioFile,
                 metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None],
                 metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None] | None = None,
                 update_using_mutagen_metadata: bool = True):
        self.audio_file = audio_file
        self.metadata_keys_direct_map_read = metadata_keys_direct_map_read
        self.metadata_keys_direct_map_write = metadata_keys_direct_map_write
        self.update_using_mutagen_metadata = update_using_mutagen_metadata

    @abstractmethod
    def _extract_mutagen_metadata(self) -> MutagenMetadata:
        raise NotImplementedError()

    @abstractmethod
    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys_and_multi_values(self) -> RawMetadataDict:
        raise NotImplementedError()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
            self, raw_clean_metadata: RawMetadataDict, app_metadata_key: AppMetadataKey) -> AppMetadataValue:
        raise NotImplementedError()

    @abstractmethod
    def _update_undirectly_mapped_metadata(
            self, app_metadata_value: AppMetadataValue, app_metadata_key: AppMetadataKey):
        raise NotImplementedError()

    @abstractmethod
    def _update_formatted_value_in_raw_mutagen_metadata(
            self, raw_metadata_key: RawMetadataKey, app_metadata_value: AppMetadataValue):
        raise NotImplementedError()

    @abstractmethod
    def _update_not_using_mutagen_metadata(self, app_metadata: AppMetadata):
        raise NotImplementedError()

    def _get_cleaned_raw_metadata_from_file(self) -> RawMetadataDict:
        self.raw_mutagen_metadata = self._extract_mutagen_metadata()
        raw_clean_metadata_with_potential_duplicate_keys_and_multi_values = \
            self._convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys_and_multi_values()

        return self._extract_and_regroup_raw_metadata_unique_entries(
            raw_clean_metadata_with_potential_duplicate_keys_and_multi_values)

    def _extract_and_regroup_raw_metadata_unique_entries(
            self, raw_clean_metadata_with_potential_duplicate_keys_and_multi_values: RawMetadataDict):
        raw_clean_metadata_with_regrouped_lists = {}
        for raw_metadata_key, raw_metadata_value in raw_clean_metadata_with_potential_duplicate_keys_and_multi_values.items():
            if isinstance(raw_metadata_value, list):
                raw_clean_metadata_with_regrouped_lists[raw_metadata_key] = raw_metadata_value
            else:
                raw_clean_metadata_with_regrouped_lists[raw_metadata_key] = [raw_metadata_value]
        return raw_clean_metadata_with_regrouped_lists

    def get_app_metadata(self) -> AppMetadata:
        if not self.raw_clean_metadata:
            self.raw_clean_metadata = self._get_cleaned_raw_metadata_from_file()

        app_metadata = {}
        for metadata_key in self.metadata_keys_direct_map_read:
            app_metadata_value = self.get_app_specific_metadata(metadata_key)
            if app_metadata_value is not None:
                app_metadata[metadata_key] = app_metadata_value
        return app_metadata

    def get_app_specific_metadata(self, app_metadata_key: AppMetadataKey) -> AppMetadataValue:
        if not self.raw_clean_metadata:
            self.raw_clean_metadata = self._get_cleaned_raw_metadata_from_file()

        if app_metadata_key not in self.metadata_keys_direct_map_read:
            raise MetadataNotSupportedError(f'{app_metadata_key} metadata not supported by this format')

        raw_metadata_key = self.metadata_keys_direct_map_read[app_metadata_key]
        if not raw_metadata_key:
            return self._get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
                raw_clean_metadata=self.raw_clean_metadata, app_metadata_key=app_metadata_key)

        value = self.raw_clean_metadata.get(raw_metadata_key)

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
                for str_with_potential_separated_values in values_list_str:
                    separated_values = str_with_potential_separated_values.split(METADATA_ARTISTS_SEPARATION_CHAR)
                    values_list_str_with_separated_values_processed.extend(separated_values)
                return values_list_str_with_separated_values_processed
            return values_list_str
        raise ImproperlyConfigured(f'Unsupported metadata type: {app_metadata_key_optional_type}')

    def update_file_metadata(self, app_metadata: AppMetadata):
        if not self.metadata_keys_direct_map_write:
            raise MetadataNotSupportedError('This format does not support metadata modification')

        if not self.update_using_mutagen_metadata:
            self._update_not_using_mutagen_metadata(app_metadata)
        else:
            if not self.raw_mutagen_metadata:
                self.raw_mutagen_metadata = self._extract_mutagen_metadata()

            for app_metadata_key in list(app_metadata.keys()):
                app_metadata_value = app_metadata[app_metadata_key]
                if app_metadata_key not in self.metadata_keys_direct_map_write:
                    raise MetadataNotSupportedError(f'{app_metadata_key} metadata not supported by this format')
                else:
                    raw_metadata_key = self.metadata_keys_direct_map_write[app_metadata_key]
                    if raw_metadata_key:
                        self._update_formatted_value_in_raw_mutagen_metadata(
                            raw_metadata_key=raw_metadata_key, app_metadata_value=app_metadata_value)
                    else:
                        self._update_undirectly_mapped_metadata(
                            app_metadata_value=app_metadata_value, app_metadata_key=app_metadata_key)
            self.raw_mutagen_metadata.save(self.audio_file.get_file_path_or_object())

    def delete_metadata(self) -> bool:
        if not self.raw_mutagen_metadata:
            self.raw_mutagen_metadata = self._extract_mutagen_metadata()

        try:
            self.raw_mutagen_metadata.delete()
            return True
        except Exception:
            return False
