
import hashlib
from io import BufferedReader
import os
from abc import abstractmethod
from contextlib import redirect_stderr, redirect_stdout
from typing import Dict, Optional, Union

from mutagen._file import FileType
from pydub.utils import mediainfo
from tinytag import TinyTag, TinyTagException

from django.core.files.uploadedfile import InMemoryUploadedFile

from ..utils.types import AppMetadataDict, AppMetadataValue, RawMetadataDict, RawMetadataKey, RawMetadataValue
from ..utils.AudioFile import AudioFile
from ..utils.AppMetadataKey import AppMetadataKey
from ..exceptions import DurationNotFoundError, UnsupportedMetadataError

METADATA_ARTISTS_SEPARATION_CHAR = ","


class MetadataManager:

    audio_file: AudioFile
    metadata_keys_direct_map_read: Dict[AppMetadataKey, RawMetadataKey | None]
    metadata_keys_direct_map_write: Dict[AppMetadataKey, RawMetadataKey | None]
    file_raw_metadata: FileType
    raw_metadata_dict: Dict[RawMetadataKey, RawMetadataValue]

    def __init__(
            self, audio_file: AudioFile,
            metadata_keys_direct_map_read: Dict[AppMetadataKey, RawMetadataKey | None],
            metadata_keys_direct_map_write: Dict[AppMetadataKey, RawMetadataKey | None]):
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

    def _compute_md5_from_buffer(self, buffer: Union[BufferedReader, InMemoryUploadedFile]):
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: buffer.read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _set_value_in_raw_metadata_without_saving(self, raw_metadata_key: RawMetadataKey, value: AppMetadataValue):
        self.file_raw_metadata[raw_metadata_key] = value

    def _get_duration_using_mutagen(self) -> Optional[float]:
        if hasattr(self.file_raw_metadata, 'info'):
            return self.file_raw_metadata.info.length  # type: ignore
        return None

    def _get_duration_using_tinytag(self) -> Optional[int]:
        try:
            file_path_or_object = self.audio_file.get_file_path_or_object()
            with open(os.devnull, 'w') as devnull, redirect_stdout(devnull), redirect_stderr(devnull):
                return TinyTag.get(file_path_or_object).duration
        except TinyTagException as exception:
            if exception.args[0] == 'No tag reader found to support filetype! ':
                return None
            else:
                raise exception

        return TinyTag.get(self.audio_file.get_file_name()).duration

    def _get_duration_using_pydub(self) -> str:
        file_path_or_object = self.audio_file.get_file_path_or_object()
        audio_info = mediainfo(file_path_or_object)
        return audio_info['duration']

    def get_duration_in_sec(self) -> int:
        duration_in_sec_float = self._get_duration_using_mutagen()
        duration_in_sec = int(duration_in_sec_float) if duration_in_sec_float else None
        if duration_in_sec is None:
            duration_in_sec_float = self._get_duration_using_tinytag()
            duration_in_sec = int(duration_in_sec_float) if duration_in_sec_float else None

        if duration_in_sec is None:
            duration_in_sec_float = self._get_duration_using_pydub()
            duration_in_sec = int(float(duration_in_sec_float))

        if duration_in_sec == 0:
            duration_in_sec = 1
        elif duration_in_sec is None:
            raise DurationNotFoundError("Duration not found in metadata.")
        return duration_in_sec

    def get_app_metadata_dict(self, normalized_rating_max_value: Optional[int] = None) -> AppMetadataDict:
        app_metadata_dict = {}
        for format_supported_metadata_key in self.metadata_keys_direct_map_read:
            app_metadata_dict[format_supported_metadata_key] = self.get_specific_metadata(
                format_supported_metadata_key, normalized_rating_max_value)
        return app_metadata_dict

    def get_specific_metadata(
            self, app_metadata_key: AppMetadataKey, normalized_rating_max_value: Optional[int] = None):
        if app_metadata_key not in self.metadata_keys_direct_map_read:
            raise UnsupportedMetadataError(f'{app_metadata_key.value} metadata not supported by this format')

        value = self.metadata_keys_direct_map_read[app_metadata_key]
        if not value:
            return self._get_undirectly_mapped_metadata_value(app_metadata_key)

    def update_bulk(self, app_metadata_dict: AppMetadataDict):
        for app_metadata_key in list(app_metadata_dict.keys()):
            value = app_metadata_dict[app_metadata_key]
            if app_metadata_key not in self.metadata_keys_direct_map_write:
                raise UnsupportedMetadataError(f'{app_metadata_key.value} metadata not supported by this format')
            else:
                raw_metadata_key = self.metadata_keys_direct_map_write[app_metadata_key]
                if raw_metadata_key:
                    self._set_value_in_raw_metadata_without_saving(raw_metadata_key=raw_metadata_key, value=value)
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
