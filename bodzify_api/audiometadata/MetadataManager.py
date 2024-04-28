#!/usr/bin/env python

from abc import abstractmethod
from typing import Optional
from tinytag import TinyTag
import tempfile

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile


class NormalizedMetadataKeys:
    TITLE = 'title'
    ARTIST_NAME = 'artist_name'
    ALBUM_NAME = 'album_name'
    ALBUM_ARTISTS_NAMES = 'album_artists_names_string'
    GENRE_NAME = 'genre_name'
    DURATION = 'duration'
    RATING = 'rating'
    LANGUAGE = 'language'


METADATA_ARTISTS_SEPARATION_CHAR = ","


class MetadataManager:
    BASE_255_RATING_STAR_VALUES = [0, 13, 1, 54, 64, 118, 128, 186, 196, 242, 255]
    BASE_255_PROPORTIONAL_RATING_STAR_VALUES = [None, None, 51, None, 102, None, 153, None, 204, None, 255]
    BASE_100_RATING_STAR_VALUES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

    METADATA_CANNOT_BE_SET_MESSAGE = "This metadata cannot be updated. It is therefore ignored."
    METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified metadata key is not handled by the service."""

    class RatingFileProfile:
        BASE_255 = '255'
        BASE_100 = '100'

    file: object
    file_metadata: dict

    def __init__(self, file):
        self.file = file
        self.file_metadata = self._get_file_metadata(file)

    @abstractmethod
    def _get_file_metadata(self, file) -> dict:
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_title(self):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_artist_name(self):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_album_name(self):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_album_artists_name_str(self):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_genre_name(self):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_eventually_normalized_rating_value_from_file_metadata(
            self, normalized_rating_max_value: Optional[int] = None):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_language() -> Optional[str]:
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def get_specific_file_metadata(
            self, normalized_metadata_key: str, normalized_rating_max_value: Optional[int] = None):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def update_specific_file_metadata(self,
                                      normalized_metadata_value,
                                      normalized_metadata_key: str,
                                      normalized_rating_max_value: int):
        raise NotImplementedError("This method must be implemented.")

    @abstractmethod
    def update_file_metadata(self, normalized_metadata, normalized_rating_max_value: int):
        raise NotImplementedError("This method must be implemented.")

    def _get_first_value_str_if_exists_in_file_metadata_or_none(self, key: str):
        if key in self.file_metadata:
            return self.file_metadata[key][0]
        else:
            return None

    def _get_first_value_int_if_exists_in_file_metadata_or_none(self, key: str):
        if key in self.file_metadata:
            value_str = self.file_metadata[key][0]
            if value_str != "":
                return int(value_str)
        return None

    def _get_eventually_normalized_rating_from_file_metadata_value(self,
                                                                   file_rating_value: int,
                                                                   normalized_rating_max_value: Optional[int] = None,
                                                                   is_rating_from_traktor: bool = False):
        if file_rating_value is not None:
            if normalized_rating_max_value is not None:
                if file_rating_value == 0 and is_rating_from_traktor:
                    return None
                for star_rating_base_10 in range(11):
                    if file_rating_value in [self.BASE_255_RATING_STAR_VALUES[star_rating_base_10],
                                             self.BASE_255_PROPORTIONAL_RATING_STAR_VALUES[star_rating_base_10],
                                             self.BASE_100_RATING_STAR_VALUES[star_rating_base_10]]:
                        return int(star_rating_base_10 * normalized_rating_max_value / 10)
                raise ValueError("Rating value not handled: " + str(file_rating_value))
            else:
                return file_rating_value
        else:
            return None

    def _get_file_rating_from_normalized_value(self,
                                               normalized_rating: int,
                                               normalized_rating_max_value: int,
                                               rating_file_profile: str):
        star_rating_base_10 = (int)((normalized_rating * 10)/normalized_rating_max_value)
        if rating_file_profile == self.RatingFileProfile.BASE_255:
            return self.BASE_255_RATING_STAR_VALUES[star_rating_base_10]
        else:
            return self.BASE_100_RATING_STAR_VALUES[star_rating_base_10]

    def _get_duration_from_file_matadata(self) -> Optional[float]:
        if hasattr(self.file_metadata, 'info'):
            return self.file_metadata.info.length
        return None

    def _get_duration_using_tinytag(self) -> Optional[float]:
        if isinstance(self.file, TemporaryUploadedFile):
            with open(self.file.temporary_file_path(), 'rb') as f:
                return TinyTag.get(f.name).duration
        elif isinstance(self.file, FieldFile):
            with open(self.file.path, 'rb') as f:
                return TinyTag.get(f.name).duration
        elif isinstance(self.file, InMemoryUploadedFile):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in self.file.chunks():
                    tmp.write(chunk)
                tmp.close()
                return TinyTag.get(tmp.name).duration
        return TinyTag.get(self.file.name).duration

    def get_duration(self):
        duration = self._get_duration_from_file_matadata()
        if duration is None:
            duration = self._get_duration_using_tinytag()
        return duration
