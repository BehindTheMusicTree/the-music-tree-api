#!/usr/bin/env python

import io
from typing import Optional

from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            TemporaryUploadedFile)
from django.db.models.fields.files import FieldFile
from mutagen._file import FileType as MutagenFileMetadata
from mutagen.flac import FLAC

from bodzify_api.utils.audio_metadata.MetadataManager import (
    MetadataManager, NormalizedMetadataKeys)


# Flac files
class VorbisManager(MetadataManager):

    class VorbisTagKeys:
        TITLE = 'title'
        ARTIST_NAME = 'artist'
        ALBUM_NAME = 'album'
        ALBUM_ARTISTS_NAMES = 'albumartist'
        GENRE_NAME = 'genre'
        RATING = 'rating'
        RATING_TRAKTOR = 'rating wmp'
        LANGUAGE = 'language'

    def __init__(self, file):
        super().__init__(file)

    def _get_file_metadata(self) -> MutagenFileMetadata:
        if isinstance(self.file, TemporaryUploadedFile):
            with open(self.file.temporary_file_path(), 'rb') as f:
                return FLAC(fileobj=io.BytesIO(f.read()))
        elif isinstance(self.file, FieldFile):
            with open(self.file.path, 'rb') as f:
                return FLAC(fileobj=f)
        elif isinstance(self.file, InMemoryUploadedFile):
            self.file.seek(0)
            return FLAC(io.BytesIO(self.file.read()))
        with open(self.file, 'rb') as f:  # type: ignore
            return FLAC(fileobj=f)

    def get_eventually_normalized_rating_value(self,
                                               normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        file_rating = self._get_first_value_int_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.RATING)
        is_rating_from_traktor = False
        if file_rating is None:
            file_rating = self._get_first_value_int_if_exists_in_file_metadata_or_none(
                key=self.VorbisTagKeys.RATING_TRAKTOR)
            if file_rating is not None:
                is_rating_from_traktor = True

        if file_rating is None or file_rating == "":
            return None
        else:
            return self._get_eventually_normalized_rating_from_file_rating(
                file_rating=file_rating,
                is_rating_from_traktor=is_rating_from_traktor,
                normalized_rating_max_value=normalized_rating_max_value)

    def get_title(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.TITLE)

    def get_artist_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.ARTIST_NAME)

    def get_album_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        album_artists_name_str_raw = self._get_first_value_str_if_exists_in_file_metadata_or_none(
            key=self.VorbisTagKeys.ALBUM_ARTISTS_NAMES)
        if album_artists_name_str_raw is not None:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> Optional[str]:
        if self.VorbisTagKeys.GENRE_NAME in self.file_metadata:
            return self.file_metadata[self.VorbisTagKeys.GENRE_NAME][0]
        else:
            return ""

    def get_language(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.LANGUAGE)

    def get_bitrate(self):
        return self.file_metadata.info.bitrate / 1000  # type: ignore

    def update_specific_file_metadata_without_saving(
            self,
            normalized_metadata_value,
            normalized_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        if normalized_metadata_key == NormalizedMetadataKeys.TITLE:
            vorbis_tag_key = self.VorbisTagKeys.TITLE
        elif normalized_metadata_key == NormalizedMetadataKeys.ARTIST_NAME:
            vorbis_tag_key = self.VorbisTagKeys.ARTIST_NAME
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_NAME:
            vorbis_tag_key = self.VorbisTagKeys.ALBUM_NAME
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES:
            vorbis_tag_key = self.VorbisTagKeys.ALBUM_ARTISTS_NAMES
        elif normalized_metadata_key == NormalizedMetadataKeys.GENRE_NAME:
            vorbis_tag_key = self.VorbisTagKeys.GENRE_NAME
        elif normalized_metadata_key == NormalizedMetadataKeys.RATING:
            app_rating = normalized_metadata_value
            vorbis_tag_key = self.VorbisTagKeys.RATING
            if app_rating is not None:
                vorbis_rating = self._get_file_rating_from_normalized_rating(
                    normalized_rating=app_rating,
                    normalized_rating_max_value=normalized_rating_max_value,  # type: ignore
                    rating_file_profile=self.RatingFileProfile.BASE_100)
                normalized_metadata_value = str(vorbis_rating)
        elif normalized_metadata_key == NormalizedMetadataKeys.LANGUAGE:
            vorbis_tag_key = self.VorbisTagKeys.LANGUAGE
        else:
            raise KeyError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        if normalized_metadata_value is not None:
            if vorbis_tag_key not in self.file_metadata:
                self.file_metadata[vorbis_tag_key] = [1]
            self.file_metadata[vorbis_tag_key] = normalized_metadata_value
        elif vorbis_tag_key in self.file_metadata:
            del self.file_metadata[vorbis_tag_key]
