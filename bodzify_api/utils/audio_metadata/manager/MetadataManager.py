
import hashlib
from io import BufferedReader
import os
from abc import abstractmethod
from contextlib import redirect_stderr, redirect_stdout
from typing import Optional, Union
from pydub.utils import mediainfo
from tinytag import TinyTag, TinyTagException

from django.core.files.uploadedfile import InMemoryUploadedFile

from bodzify_api.utils.audio_metadata.audio_file import AudioFile

from ..app_metadata_keys import AppMetadataKeys

METADATA_ARTISTS_SEPARATION_CHAR = ","


class MetadataManager:
    BASE_255_RATING_STAR_VALUES = [0, 13, 1, 54, 64, 118, 128, 186, 196, 242, 255]
    BASE_255_PROPORTIONAL_RATING_STAR_VALUES = [None, None, 51, None, 102, None, 153, None, 204, None, 255]
    BASE_100_RATING_STAR_VALUES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

    METADATA_CANT_BE_UPDATED_MESSAGE = "This metadata cannot be updated. It is therefore ignored."
    METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified metadata key is not handled by the service."""

    class RatingFileProfile:
        BASE_255 = '255'
        BASE_100 = '100'

    audio_file: AudioFile
    file_raw_metadata: dict

    def __init__(self, audio_file: AudioFile):
        self.audio_file = audio_file
        self.file_raw_metadata = self.get_raw_metadata()

    @abstractmethod
    def get_raw_metadata(self) -> dict:
        raise NotImplementedError(f"{self.get_raw_metadata.__name__} method must be implemented.")

    def _compute_md5_from_buffer(self, buffer: Union[BufferedReader, InMemoryUploadedFile]):
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: buffer.read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @abstractmethod
    def get_title(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_title.__name__} method must be implemented.")

    @abstractmethod
    def get_artists_names(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_artists_names.__name__} method must be implemented.")

    @abstractmethod
    def get_album_name(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_album_name.__name__} method must be implemented.")

    @abstractmethod
    def get_album_artists_name_str(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_album_artists_name_str.__name__} method must be implemented.")

    @abstractmethod
    def get_genre_name(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_genre_name.__name__} method must be implemented.")

    @abstractmethod
    def get_eventually_normalized_rating_value(self,
                                               normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        raise NotImplementedError(
            f"{self.get_eventually_normalized_rating_value.__name__} method must be implemented.")

    @abstractmethod
    def get_language(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_language.__name__} method must be implemented.")

    @abstractmethod
    def get_release_date(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_release_date.__name__} method must be implemented.")

    @abstractmethod
    def get_position_in_album(self) -> Optional[int]:
        """Get track number/position in album.

        Returns:
            Optional[int]: Track number if available, None otherwise
        """
        raise NotImplementedError(f"{self.get_position_in_album.__name__} method must be implemented.")

    @abstractmethod
    def get_bpm(self) -> Optional[float]:
        """Get BPM (Beats Per Minute) value.

        Returns:
            Optional[float]: BPM value if available, None otherwise
        """
        raise NotImplementedError(f"{self.get_bpm.__name__} method must be implemented.")

    @abstractmethod
    def update_specific_file_metadata_without_saving(self,
                                                     normalized_metadata_value,
                                                     normalized_metadata_key: str,
                                                     normalized_rating_max_value: Optional[int] = None):
        raise NotImplementedError(
            f"{self.update_specific_file_metadata_without_saving.__name__} method must be implemented.")

    def _get_first_value_str_if_exists_in_file_metadata_or_none(self, key: str):
        if key in self.file_raw_metadata:
            return self.file_raw_metadata[key][0]
        else:
            return None

    def _get_first_value_int_if_exists_in_file_metadata_or_none(self, key: str):
        if key in self.file_raw_metadata:
            value_str = self.file_raw_metadata[key][0]
            if value_str != "":
                return int(value_str)
        return None

    def _get_eventually_normalized_rating_from_file_rating(self,
                                                           file_rating: int,
                                                           normalized_rating_max_value: Optional[int] = None,
                                                           is_rating_from_traktor: bool = False):
        if file_rating is not None:
            if normalized_rating_max_value:
                if file_rating == 0 and is_rating_from_traktor:
                    return None
                for star_rating_base_10 in range(11):
                    if file_rating in [self.BASE_255_RATING_STAR_VALUES[star_rating_base_10],
                                       self.BASE_255_PROPORTIONAL_RATING_STAR_VALUES[star_rating_base_10],
                                       self.BASE_100_RATING_STAR_VALUES[star_rating_base_10]]:
                        return int(star_rating_base_10 * normalized_rating_max_value / 10)
                raise ValueError("Rating value not handled: " + str(file_rating))
            else:
                return file_rating
        else:
            return None

    def _get_file_rating_from_normalized_rating(self,
                                                normalized_rating: int,
                                                normalized_rating_max_value: int,
                                                rating_file_profile: str):
        star_rating_base_10 = (int)((normalized_rating * 10)/normalized_rating_max_value)
        if rating_file_profile == self.RatingFileProfile.BASE_255:
            return self.BASE_255_RATING_STAR_VALUES[star_rating_base_10]
        else:
            return self.BASE_100_RATING_STAR_VALUES[star_rating_base_10]

    def _get_duration_from_file_matadata_using_mutagen(self) -> Optional[float]:
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
        duration_in_sec_float = self._get_duration_from_file_matadata_using_mutagen()
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
            raise Exception("Duration not found in metadata.")
        return duration_in_sec

    def get_normalized_metadata(self, normalized_rating_max_value: Optional[int] = None) -> dict:
        normalized_metadata = dict()
        normalized_metadata[AppMetadataKeys.TITLE] = self.get_title()
        normalized_metadata[AppMetadataKeys.ARTISTS_NAMES_STR] = self.get_artists_names()
        normalized_metadata[AppMetadataKeys.ALBUM_NAME] = self.get_album_name()
        normalized_metadata[AppMetadataKeys.ALBUM_ARTISTS_NAMES_STR] = self.get_album_artists_name_str()
        normalized_metadata[AppMetadataKeys.GENRE_NAME] = self.get_genre_name()
        normalized_metadata[AppMetadataKeys.DURATION_IN_SEC] = self.get_duration_in_sec()
        normalized_metadata[AppMetadataKeys.RATING] = self.get_eventually_normalized_rating_value(
            normalized_rating_max_value=normalized_rating_max_value)
        normalized_metadata[AppMetadataKeys.LANGUAGE] = self.get_language()
        normalized_metadata[AppMetadataKeys.RELEASE_DATE] = self.get_release_date()
        normalized_metadata[AppMetadataKeys.POSITION_IN_ALBUM] = self.get_position_in_album()
        normalized_metadata[AppMetadataKeys.BPM] = self.get_bpm()
        return normalized_metadata

    def get_specific_file_metadata(self, normalized_metadata_key: str,
                                   normalized_rating_max_value: Optional[int] = None):
        if normalized_metadata_key == AppMetadataKeys.TITLE:
            return self.get_title()
        elif normalized_metadata_key == AppMetadataKeys.ARTISTS_NAMES_STR:
            return self.get_artists_names()
        elif normalized_metadata_key == AppMetadataKeys.ALBUM_NAME:
            return self.get_album_name()
        elif normalized_metadata_key == AppMetadataKeys.ALBUM_ARTISTS_NAMES_STR:
            return self.get_album_artists_name_str()
        elif normalized_metadata_key == AppMetadataKeys.GENRE_NAME:
            return self.get_genre_name()
        elif normalized_metadata_key == AppMetadataKeys.DURATION_IN_SEC:
            return self.get_duration_in_sec()
        elif normalized_metadata_key == AppMetadataKeys.RATING:
            return self.get_eventually_normalized_rating_value(normalized_rating_max_value)
        elif normalized_metadata_key == AppMetadataKeys.LANGUAGE:
            return self.get_language()
        elif normalized_metadata_key == AppMetadataKeys.RELEASE_DATE:
            return self.get_release_date()
        elif normalized_metadata_key == AppMetadataKeys.POSITION_IN_ALBUM:
            return self.get_position_in_album()
        elif normalized_metadata_key == AppMetadataKeys.BPM:
            return self.get_bpm()

    def update_file_metadata(self, normalized_metadata: dict, normalized_rating_max_value: Optional[int]):
        for key in list(normalized_metadata.keys()):
            if key == AppMetadataKeys.DURATION_IN_SEC:
                raise ValueError(self.METADATA_CANT_BE_UPDATED_MESSAGE)
            else:
                value = normalized_metadata[key]
                if key == AppMetadataKeys.RATING:
                    if normalized_rating_max_value is None:
                        raise Exception("If updating the rating, the max value of the normalized rating must be set.")
                    self.update_specific_file_metadata_without_saving(
                        normalized_metadata_value=value,
                        normalized_metadata_key=key,
                        normalized_rating_max_value=normalized_rating_max_value)
                else:
                    self.update_specific_file_metadata_without_saving(normalized_metadata_value=value,
                                                                      normalized_metadata_key=key)

        self.file_raw_metadata.save(self.audio_file.path)  # type: ignore
