#!/usr/bin/env python

from typing import Optional

from mutagen.id3._frames import POPM, TALB, TCON, TIT2, TLAN, TPE1, TPE2

from ..NormalizedMetadataKeys import NormalizedMetadataKeys
from ..MetadataManager import MetadataManager

ID3_RATING_APP_EMAIL = 'bodzify'


class Id3Manager(MetadataManager):

    class Id3TextFrames:  # MP3 and Wave (.wav) files use ID3 tags
        TITLE = 'TIT2'
        ARTIST_NAME = 'TPE1'
        ALBUM_NAME = 'TALB'
        ALBUM_ARTISTS_NAMES = 'TPE2'
        GENRE_NAME = 'TCON'
        RATING = 'POPM'
        LANGUAGE = 'TLAN'

    def __init__(self, file):
        super().__init__(file)

    def get_title(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(self.Id3TextFrames.TITLE)

    def get_artists_names(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(self.Id3TextFrames.ARTIST_NAME)

    def get_album_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(self.Id3TextFrames.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        album_artists_name_str_raw = (self._get_first_value_str_if_exists_in_file_metadata_or_none(
            self.Id3TextFrames.ALBUM_ARTISTS_NAMES))
        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> Optional[str]:
        if self.Id3TextFrames.GENRE_NAME in self.file_metadata:
            return self.file_metadata[self.Id3TextFrames.GENRE_NAME][0]
        else:
            return ""

    def get_eventually_normalized_rating_value(self, normalized_rating_max_value: Optional[int] = None):
        file_rating_value = None
        file_rating_email = None
        for key in self.file_metadata:
            if self.Id3TextFrames.RATING in key:
                file_rating_tag = self.file_metadata[key]
                file_rating_email = file_rating_tag.email
                file_rating_value = file_rating_tag.rating
        if file_rating_value is None:
            return None
        else:
            return self._get_eventually_normalized_rating_from_file_rating(
                file_rating=file_rating_value,
                is_rating_from_traktor=(file_rating_email == self.TRAKTOR_RATING_TAG_MAIL),
                normalized_rating_max_value=normalized_rating_max_value)

    def get_language(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.Id3TextFrames.LANGUAGE)

    def update_specific_file_metadata_without_saving(
            self,
            normalized_metadata_value,
            normalized_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        if normalized_metadata_key == NormalizedMetadataKeys.TITLE:
            id3_key = self.Id3TextFrames.TITLE
            text_frame_class = TIT2
        elif normalized_metadata_key == NormalizedMetadataKeys.ARTISTS_NAMES:
            id3_key = self.Id3TextFrames.ARTIST_NAME
            text_frame_class = TPE1
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_NAME:
            id3_key = self.Id3TextFrames.ALBUM_NAME
            text_frame_class = TALB
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES:
            id3_key = self.Id3TextFrames.ALBUM_ARTISTS_NAMES
            text_frame_class = TPE2
        elif normalized_metadata_key == NormalizedMetadataKeys.GENRE_NAME:
            id3_key = self.Id3TextFrames.GENRE_NAME
            text_frame_class = TCON
        elif normalized_metadata_key == NormalizedMetadataKeys.RATING:
            normalized_rating = normalized_metadata_value
            self.file_metadata.delall(self.Id3TextFrames.RATING)  # type: ignore
            if normalized_rating:
                id3_rating = self._get_file_rating_from_normalized_rating(
                    normalized_rating=normalized_rating,
                    normalized_rating_max_value=normalized_rating_max_value,
                    rating_file_profile=self.RatingFileProfile.BASE_255)
                self.file_metadata.add(POPM(email=ID3_RATING_APP_EMAIL, rating=id3_rating))  # type: ignore
            return
        elif normalized_metadata_key == NormalizedMetadataKeys.LANGUAGE:
            id3_key = self.Id3TextFrames.LANGUAGE
            text_frame_class = TLAN
        else:
            raise KeyError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        self.file_metadata.delall(id3_key)  # type: ignore
        self.file_metadata.add(text_frame_class(encoding=3, text=normalized_metadata_value))  # type: ignore
