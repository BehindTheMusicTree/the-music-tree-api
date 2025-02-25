
from typing import Optional, Tuple, Type, TypeVar

from mutagen._file import FileType
from mutagen.flac import FLAC, VCFLACDict

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils import data_transformer

from ...utils.AudioFile import AudioFile
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadataValue, RawMetadataDict, RawMetadataKey
from ...exceptions import FileCorruptedError, InvalidChunkDecodeError
from ..MetadataManager import AppMetadataKey
from .RatingSupportingMetadataManager import RatingSupportingMetadataManager


class VorbisManager(RatingSupportingMetadataManager):
    """
    Manages Vorbis comments for audio files.

    Vorbis comments are used to store metadata in audio files, primarily in formats like Ogg Vorbis and FLAC.
    They are more flexible and extensible compared to ID3 tags, allowing for a wide range of metadata fields.

    Genre Support:
    Like ID3v2 but unlike ID3v1 and RIFF, Vorbis comments support:
    - Custom genre names as free text
    - Multiple genres (comma-separated)
    - No length limitations
    - Unicode support for international genres
    - No predefined genre list restrictions

    Vorbis comments are key-value pairs, where the key is a field name and the value is the corresponding metadata.
    Common fields are defined in the VorbisKey enum class, which includes standardized keys for metadata like
    title, artist, album, genre, rating, and more.

    Compatible Extensions:
    - Ogg Vorbis: Fully supports Vorbis comments.
    - FLAC: Fully supports Vorbis comments.
    - Opus: Fully supports Vorbis comments.

    Note: This class assumes that the audio files being managed are primarily in formats that support Vorbis comments.
    """

    class VorbisKey(RawMetadataKey):
        TITLE = 'title'
        ARTIST_NAME = 'artist'
        ALBUM_NAME = 'album'
        ALBUM_ARTISTS_NAMES = 'albumartist'
        GENRE_NAME = 'genre'
        RATING = 'rating'
        RATING_TRAKTOR = 'rating wmp'  # Traktor rating
        LANGUAGE = 'language'
        DATE = 'date'  # Creation/Release date
        TRACK_NUMBER = 'tracknumber'
        BPM = 'bpm'
        COMMENT = 'comment'
        COMPOSER = 'composer'
        PERFORMER = 'performer'
        COPYRIGHT = 'copyright'
        LICENSE = 'license'
        ORGANIZATION = 'organization'  # Label or organization
        DESCRIPTION = 'description'
        LOCATION = 'location'  # Recording location
        CONTACT = 'contact'  # Contact information
        ISRC = 'isrc'  # International Standard Recording Code
        ENCODED_BY = 'encodedby'  # Encoder software

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: int | None = None):
        metadata_keys_direct_map_read = {
            AppMetadataKey.TITLE: self.VorbisKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.VorbisKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.VorbisKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: None,
            AppMetadataKey.GENRE_NAME: None,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
        }
        metadata_keys_direct_map_write = {
            AppMetadataKey.TITLE: self.VorbisKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.VorbisKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.VorbisKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: self.VorbisKey.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: self.VorbisKey.GENRE_NAME,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_100_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_raw_metadata(self) -> FileType:
        try:
            return FLAC(self.audio_file.get_file_path_or_object())
        except Exception as error:
            error_str = str(error)
            if "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
                raise InvalidChunkDecodeError(error_str)
            raise

    def _convert_raw_metadata_to_dict(self) -> RawMetadataDict:
        file_raw_metadata_flac: FLAC = self.file_raw_metadata  # type: ignore
        metadata = file_raw_metadata_flac.tags
        if isinstance(metadata, dict):
            return metadata
        elif isinstance(metadata, VCFLACDict):
            return dict(metadata)
        elif not metadata:
            return {}
        else:
            raise FileCorruptedError(f"Invalid Vorbis metadata type: {type(metadata)}")

    def _extract_file_rating_by_traktor_or_not(self) -> Tuple[int | None, bool]:
        rating = data_transformer.get_first_value_int_if_exists_in_str_dict_or_none(
            str_dict=self.raw_metadata_dict, key=self.VorbisKey.RATING.value)

        if rating:
            return rating, False

        rating = data_transformer.get_first_value_int_if_exists_in_str_dict_or_none(
            str_dict=self.raw_metadata_dict, key=self.VorbisKey.RATING_TRAKTOR.value)
        if rating:
            return rating, True

        return None, False

    def _get_undirectly_mapped_metadata_value_other_than_rating(
            self, app_metadata_key: AppMetadataKey) -> Optional[AppMetadataValue]:
        if app_metadata_key == AppMetadataKey.GENRE_NAME:
            return self._get_genre_name()
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            return self._get_album_artists_name_str()
        else:
            raise ImproperlyConfigured('Metadata key not handled')

    def _get_genre_name(self) -> str | None:
        if self.VorbisKey.GENRE_NAME.value in self.file_raw_metadata:
            genres_names = self.file_raw_metadata.get(self.VorbisKey.GENRE_NAME)
            if isinstance(genres_names, list):
                return genres_names[0]
            elif isinstance(genres_names, str):
                return genres_names
            return ""
        else:
            return ""

    def _get_album_artists_name_str(self) -> str | None:
        album_artists_name_str_raw = self.file_raw_metadata.get(self.VorbisKey.ALBUM_ARTISTS_NAMES)

        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def _update_value_in_raw_metadata(self, raw_metadata_key: RawMetadataKey, value: AppMetadataValue):
        if value:
            if raw_metadata_key not in self.file_raw_metadata:
                self.file_raw_metadata[raw_metadata_key] = [1]
            self.file_raw_metadata[raw_metadata_key] = raw_metadata_key
        elif raw_metadata_key in self.file_raw_metadata:
            del self.file_raw_metadata[raw_metadata_key]

    def _update_undirectly_mapped_metadata(self, app_metadata_value, app_metadata_key: AppMetadataKey):
        if app_metadata_key == AppMetadataKey.RATING:
            if app_metadata_value:
                app_metadata_value = str(app_metadata_value)
            self._update_value_in_raw_metadata(
                raw_metadata_key=self.VorbisKey.RATING, value=app_metadata_value)
        else:
            raise ImproperlyConfigured('Metadata key not handled')
