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

    METADATA_CANT_BE_UPDATED_MESSAGE = "This metadata cannot be updated. It is therefore ignored."
    METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE = """The specified metadata key is not handled by the service."""

    class RatingFileProfile:
        BASE_255 = '255'
        BASE_100 = '100'

    file: object
    file_metadata: dict

    def __init__(self, file):
        self.file = file
        self.file_metadata = self._get_file_metadata()

    @abstractmethod
    def _get_file_metadata(self) -> dict:
        raise NotImplementedError(f"{self._get_file_metadata.__name__} method must be implemented.")

    @abstractmethod
    def get_title(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_title.__name__} method must be implemented.")

    @abstractmethod
    def get_artist_name(self) -> Optional[str]:
        raise NotImplementedError(f"{self.get_artist_name.__name__} method must be implemented.")

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
    def update_specific_file_metadata_without_saving(self,
                                                     normalized_metadata_value,
                                                     normalized_metadata_key: str,
                                                     normalized_rating_max_value: Optional[int] = None):
        raise NotImplementedError(
            f"{self.update_specific_file_metadata_without_saving.__name__} method must be implemented.")

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

    def _get_eventually_normalized_rating_from_file_rating(self,
                                                           file_rating: int,
                                                           normalized_rating_max_value: Optional[int] = None,
                                                           is_rating_from_traktor: bool = False):
        if file_rating is not None:
            if normalized_rating_max_value is not None:
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
        if self.file.file:
            filename = self.file.file.name
        else:
            filename = self.file.name
        return TinyTag.get(filename).duration

    def get_duration(self):
        duration = self._get_duration_from_file_matadata()
        if duration is None:
            duration = self._get_duration_using_tinytag()
        return duration

    def get_normalized_metadata(self, normalized_rating_max_value: Optional[int] = None) -> dict:
        normalized_metadata = dict()
        normalized_metadata[NormalizedMetadataKeys.TITLE] = self.get_title()
        normalized_metadata[NormalizedMetadataKeys.ARTIST_NAME] = self.get_artist_name()
        normalized_metadata[NormalizedMetadataKeys.ALBUM_NAME] = self.get_album_name()
        normalized_metadata[NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES] = self.get_album_artists_name_str()
        normalized_metadata[NormalizedMetadataKeys.GENRE_NAME] = self.get_genre_name()
        normalized_metadata[NormalizedMetadataKeys.DURATION] = self.get_duration()
        normalized_metadata[NormalizedMetadataKeys.RATING] = self.get_eventually_normalized_rating_value(
            normalized_rating_max_value=normalized_rating_max_value)
        normalized_metadata[NormalizedMetadataKeys.LANGUAGE] = self.get_language()
        return normalized_metadata

    def get_specific_file_metadata(self, normalized_metadata_key: str,
                                   normalized_rating_max_value: Optional[int] = None):
        if normalized_metadata_key == NormalizedMetadataKeys.TITLE:
            return self.get_title()
        elif normalized_metadata_key == NormalizedMetadataKeys.ARTIST_NAME:
            return self.get_artist_name()
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_NAME:
            return self.get_album_name()
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES:
            return self.get_album_artists_name_str()
        elif normalized_metadata_key == NormalizedMetadataKeys.GENRE_NAME:
            return self.get_genre_name()
        elif normalized_metadata_key == NormalizedMetadataKeys.DURATION:
            return self.get_duration()
        elif normalized_metadata_key == NormalizedMetadataKeys.RATING:
            return self.get_eventually_normalized_rating_value(normalized_rating_max_value)
        elif normalized_metadata_key == NormalizedMetadataKeys.LANGUAGE:
            return self.get_language()

    def update_file_metadata(self, normalized_metadata: dict, normalized_rating_max_value: int):
        for key in list(normalized_metadata.keys()):
            if key == NormalizedMetadataKeys.DURATION:
                raise ValueError(self.METADATA_CANT_BE_UPDATED_MESSAGE)
            else:
                value = normalized_metadata[key]
                if key == NormalizedMetadataKeys.RATING:
                    self.update_specific_file_metadata_without_saving(
                        normalized_metadata_value=value,
                        normalized_metadata_key=key,
                        normalized_rating_max_value=normalized_rating_max_value)
                else:
                    self.update_specific_file_metadata_without_saving(normalized_metadata_value=value,
                                                                      normalized_metadata_key=key)

        self.file_metadata.save(self.file.path)
