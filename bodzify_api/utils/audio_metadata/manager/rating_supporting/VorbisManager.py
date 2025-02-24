from enum import Enum
import io
from typing import Dict, Optional

from mutagen.flac import FLAC, VCFLACDict
from mutagen.id3._util import ID3NoHeaderError
from mutagen.id3 import ID3

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils.audio_metadata.utils.RatingProfile import RatingProfile


from ...utils.AudioFile import AudioFile
from ...exceptions import FileCorruptedError, InvalidChunkDecodeError
from ...utils.types import AppMetadataValue, RawMetadataDict, RawMetadataKey
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
    Common fields include:
    - TITLE: The title of the track.
    - ARTIST: The artist or performer.
    - ALBUM: The name of the album.
    - TRACKNUMBER: The track number on the album.
    - GENRE: The genre name of the track.
    - DATE: The date of the recording.
    - COMMENT: Any additional comments.
    - ALBUMARTIST: The album artist.
    - COMPOSER: The composer of the track.
    - PERFORMER: The performer of the track.
    - COPYRIGHT: Copyright information.
    - LICENSE: Licensing information.
    - ORGANIZATION: The organization or label.
    - DESCRIPTION: A description of the track.
    - LOCATION: The location where the track was recorded.
    - CONTACT: Contact information.
    - ISRC: International Standard Recording Code.
    - ENCODEDBY: The person or software that encoded the track.
    - BPM: Beats per minute.
    - LANGUAGE: The language of the track.
    - RATING: The rating of the track.

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
        RATING_TRAKTOR = 'rating wmp'
        LANGUAGE = 'language'

        DATE = 'date'
        TRACK_NUMBER = 'tracknumber'
        BPM = 'bpm'

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: Optional[int] = None):
        metadata_keys_direct_map = {
            AppMetadataKey.TITLE: self.VorbisKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.VorbisKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.VorbisKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: None,
            AppMetadataKey.GENRE_NAME: None,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map=metadata_keys_direct_map,
                         rating_profile=RatingProfile.BASE_100,
                         normalized_rating_max_value=normalized_rating_max_value)

    def extract_raw_metadata_dict(self) -> RawMetadataDict:
        try:
            raw_metadata = FLAC(self.audio_file.get_file_path_or_object()).tags
            print('raw_metadata:', raw_metadata)
            print('class raw_metadata:', raw_metadata.__class__)
            if isinstance(raw_metadata, dict):
                return raw_metadata
            elif isinstance(raw_metadata, VCFLACDict):
                return dict(raw_metadata)
            elif not raw_metadata:
                return {}
            else:
                raise FileCorruptedError(f"Invalid Vorbis metadata type: {type(raw_metadata)}")
        except Exception as error:
            error_str = str(error)
            if "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
                raise InvalidChunkDecodeError(error_str)
            raise

    def _extract_file_rating(self) -> Optional[int]:
        return self._get_first_value_int_if_exists_in_raw_metadata_or_none(key=self.VorbisKey.RATING)

    def _extract_file_traktor_rating(self) -> Optional[int]:
        return self._get_first_value_int_if_exists_in_raw_metadata_or_none(key=self.VorbisKey.RATING_TRAKTOR)

    def _get_undirectly_mapped_metadata_value_other_than_rating(
            self, app_metadata_key: AppMetadataKey) -> Optional[AppMetadataValue]:
        if app_metadata_key == AppMetadataKey.GENRE_NAME:
            return self._get_genre_name()
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            return self.get_album_artists_name_str()
        else:
            raise ImproperlyConfigured('Metadata key not handled')

    def _get_genre_name(self) -> Optional[str]:
        if self.VorbisKey.GENRE_NAME.value in self.file_raw_metadata:
            genres_names = self.file_raw_metadata.get(self.VorbisKey.GENRE_NAME)
            if isinstance(genres_names, list):
                return genres_names[0]
            elif isinstance(genres_names, str):
                return genres_names
            return ""
        else:
            return ""

    def get_album_artists_name_str(self) -> Optional[str]:
        album_artists_name_str_raw = \
            self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.VorbisKey.ALBUM_ARTISTS_NAMES)

        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def update_specific_metadata_without_saving(self, app_metadata_value, app_metadata_key: AppMetadataKey):
        vorbis_key: RawMetadataKey
        if app_metadata_key == AppMetadataKey.TITLE:
            vorbis_key = self.VorbisKey.TITLE
        elif app_metadata_key == AppMetadataKey.ARTISTS_NAMES_STR:
            vorbis_key = self.VorbisKey.ARTIST_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_NAME:
            vorbis_key = self.VorbisKey.ALBUM_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            vorbis_key = self.VorbisKey.ALBUM_ARTISTS_NAMES
        elif app_metadata_key == AppMetadataKey.GENRE_NAME:
            vorbis_key = self.VorbisKey.GENRE_NAME
        elif app_metadata_key == AppMetadataKey.RATING:
            app_rating = app_metadata_value
            vorbis_key = self.VorbisKey.RATING
            if app_rating:
                vorbis_rating = self._convert_normalized_rating_to_file_rating(
                    normalized_rating=app_rating, rating_profile=RatingProfile.BASE_100)
                app_metadata_value = str(vorbis_rating)
        elif app_metadata_key == AppMetadataKey.LANGUAGE:
            vorbis_key = self.VorbisKey.LANGUAGE
        elif app_metadata_key == AppMetadataKey.RELEASE_DATE:
            vorbis_key = self.VorbisKey.DATE
        elif app_metadata_key == AppMetadataKey.TRACK_NUMBER:
            vorbis_key = self.VorbisKey.TRACK_NUMBER
        elif app_metadata_key == AppMetadataKey.BPM:
            vorbis_key = self.VorbisKey.BPM
        else:
            raise ImproperlyConfigured('Metadata key not handled')

        if app_metadata_value:
            if vorbis_key not in self.file_raw_metadata:
                self.file_raw_metadata[vorbis_key] = [1]
            self.file_raw_metadata[vorbis_key] = app_metadata_value
        elif vorbis_key in self.file_raw_metadata:
            del self.file_raw_metadata[vorbis_key]

    def delete_metadata(self) -> bool:
        """Delete all metadata from the FLAC/Vorbis file.

        This removes:
        - All Vorbis comment tags
        - All pictures/album art
        - Cuesheet if present
        - Any ID3 tags that might be present

        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Read the file into memory
            self.audio_file.seek(0)
            flac_file = FLAC(io.BytesIO(self.audio_file.read()))

            # Clear all Vorbis comments
            flac_file.tags = None

            # Clear all pictures
            flac_file.clear_pictures()

            # Clear cuesheet
            flac_file.cuesheet = None

            # Save changes back to the file
            flac_file.save(self.audio_file.file_path)

            # Also remove any ID3 tags that might be present
            try:
                id3 = ID3(self.audio_file.file_path)
                id3.delete()
            except (ID3NoHeaderError, ImportError):
                pass  # No ID3 tags present or ID3 support not available

            return True
        except Exception:
            return False
