
import hashlib
from io import BufferedReader
import os
from abc import abstractmethod
from contextlib import redirect_stderr, redirect_stdout
from typing import Dict, Optional, Union
from pydub.utils import mediainfo
from tinytag import TinyTag, TinyTagException

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..types import AppMetadataDict, MetadataValue, RawMetadataDict, RawMetadataKey
from ..AudioFile import AudioFile
from ..exceptions import DurationNotFoundError, UnsupportedMetadataError
from ..AppMetadataKey import AppMetadataKey

METADATA_ARTISTS_SEPARATION_CHAR = ","


class MetadataManager:

    audio_file: AudioFile
    file_raw_metadata: RawMetadataDict

    def __init__(self, audio_file: AudioFile, metadata_keys_direct_map: Dict[AppMetadataKey, Optional[RawMetadataKey]]):
        self.audio_file = audio_file
        self.metadata_keys_direct_map = metadata_keys_direct_map
        self.file_raw_metadata = self.extract_raw_metadata()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value(self, app_netadata_key: AppMetadataKey) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def extract_raw_metadata(self) -> RawMetadataDict:
        raise NotImplementedError(f"{self.extract_raw_metadata.__name__} method must be implemented.")

    @abstractmethod
    def delete_metadata(self) -> bool:
        """
        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        raise NotImplementedError(f"{self.delete_metadata.__name__} method must be implemented.")

    @abstractmethod
    def update_specific_without_saving(self, app_metadata_value: MetadataValue, app_metadata_key: AppMetadataKey,
                                       normalized_rating_max_value: Optional[int] = None):
        raise NotImplementedError(
            f"{self.update_specific_without_saving.__name__} method must be implemented.")

    def _compute_md5_from_buffer(self, buffer: Union[BufferedReader, InMemoryUploadedFile]):
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: buffer.read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _get_first_value_str_if_exists_in_raw_metadata_or_none(self, key: RawMetadataKey) -> Optional[str]:
        if key in self.file_raw_metadata:
            value = self.file_raw_metadata[key.value]
            if isinstance(value, list):
                return value[0] if value else None
        else:
            return None

    def _get_first_value_int_if_exists_in_raw_metadata_or_none(self, key: RawMetadataKey) -> Optional[int]:
        if key in self.file_raw_metadata:
            value = self.file_raw_metadata[key]
            if isinstance(value, list):
                value_str = value[0] if value else ""
            else:
                value_str = str(value)

            if value_str and value_str.strip():
                try:
                    return int(value_str)
                except ValueError:
                    return None
        return None

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
        for format_supported_metadata_key in self.metadata_keys_direct_map:
            app_metadata_dict[format_supported_metadata_key] = self.get_specific_metadata(
                format_supported_metadata_key, normalized_rating_max_value)
        return app_metadata_dict

    def get_specific_metadata(
            self, app_metadata_key: AppMetadataKey, normalized_rating_max_value: Optional[int] = None):
        if app_metadata_key not in self.metadata_keys_direct_map:
            raise UnsupportedMetadataError(f'{app_metadata_key.value} metadata not supported by this format')

        value = self.metadata_keys_direct_map[app_metadata_key]
        if not value:
            return self._get_undirectly_mapped_metadata_value(app_metadata_key)

    def update_bulk(self, app_metadata_dict: AppMetadataDict, normalized_rating_max_value: Optional[int]):
        for key in list(app_metadata_dict.keys()):
            value = app_metadata_dict[key]
            if key == AppMetadataKey.RATING:
                if normalized_rating_max_value is None:
                    raise ImproperlyConfigured(
                        "If updating the rating, the max value of the normalized rating must be set.")
                self.update_specific_without_saving(
                    app_metadata_value=value,
                    app_metadata_key=key,
                    normalized_rating_max_value=normalized_rating_max_value)
            else:
                self.update_specific_without_saving(app_metadata_value=value, app_metadata_key=key)

        self.file_raw_metadata.save(self.audio_file.path)  # type: ignore
