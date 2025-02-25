import io
from typing import Dict, Optional

from mutagen.wave import WAVE

from bodzify_api.utils.audio_metadata.utils.AudioFile import AudioFile
from bodzify_api.utils.audio_metadata.utils.rating_profiles import RatingWritingProfile
from bodzify_api.utils.audio_metadata.utils.types import AppMetadataValue, RawMetadataDict, RawMetadataKey

from ...utils.id3v1_and_riff_genre_code_map import ID3V1_AND_RIFF_GENRE_CODE_MAP
from ...exceptions import UnsupportedMetadataError
from ..MetadataManager import AppMetadataKey
from ..rating_supporting.RatingSupportingMetadataManager import RatingSupportingMetadataManager


class RiffManager(RatingSupportingMetadataManager):
    """
    Manages RIFF metadata for WAV audio files.

    RIFF (Resource Interchange File Format) is the standard metadata format for WAV files.
    While WAV files can technically contain ID3v2 tags, this is non-standard and less reliable.
    This manager uses the standard RIFF INFO chunk with standardized four-character codes (FourCC).

    Genre Support:
    The IGNR tag in RIFF files has two modes:
    1. Genre Code (Preferred): Uses the standard ID3v1/RIFF genre list (0-147)
       - Limited to predefined genres
       - Compatible with older software
       - No custom genres
       - No multiple genres
    2. Text Mode (Less Common): Direct genre name as text
       - Less widely supported
       - May not work with all software
       - Use genre codes for better compatibility

    Note: This manager is the preferred way to handle WAV metadata, as it uses
    the format's native metadata system rather than non-standard alternatives
    like ID3v2 tags.
    """

    class RiffTagKey(RawMetadataKey):
        # Standard
        TITLE = 'INAM'
        ARTIST_NAME = 'IART'
        ALBUM_NAME = 'IPRD'
        GENRE_NAME = 'IGNR'  # Numeric code or string
        DATE = 'ICRD'  # Creation/Release date
        TRACK_NUMBER = 'IPRT'  # Part number (track number)

        # Non-standard but commonly used
        ALBUM_ARTISTS_NAMES = 'IAAR'
        LANGUAGE = 'ILNG'

        # Less common
        COMMENTS = 'ICMT'
        ENGINEER = 'IENG'  # Engineer who worked on the track
        SOFTWARE = 'ISFT'  # Software used to create the file
        COPYRIGHT = 'ICOP'
        TECHNICIAN = 'ITCH'

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: None | int = None):
        metadata_keys_direct_map = {
            AppMetadataKey.TITLE: self.RiffTagKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.RiffTagKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.RiffTagKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: self.RiffTagKey.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: None,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            # AppMetadataKey.TRACK_NUMBER: None,
        }
        super().__init__(audio_file, metadata_keys_direct_map,
                         rating_profile=RatingWritingProfile.BASE_255,
                         normalized_rating_max_value=normalized_rating_max_value)

    def extract_raw_metadata_dict(self) -> RawMetadataDict:
        self.audio_file.seek(0)
        wave_file = WAVE(io.BytesIO(self.audio_file.read()))
        return wave_file.tags if wave_file.tags else {}

    def _get_undirectly_mapped_metadata_value_other_than_rating(self, key: AppMetadataKey) -> None | AppMetadataValue:
        if key == AppMetadataKey.GENRE_NAME:
            return self.get_genre_name()
        elif key == AppMetadataKey.TRACK_NUMBER:
            return self.get_track_number()
        else:
            raise UnsupportedMetadataError(f'Metadata key not handled: {key}')

    def get_genre_name(self) -> Optional[str]:
        """
        The IGNR tag in RIFF files typically contains a genre code
        that corresponds to the ID3v1 genre list. This method converts
        the code to a human-readable genre name.
        """
        if self.RiffTagKey.GENRE_NAME in self.file_raw_metadata:
            raw_value = self.file_raw_metadata[self.RiffTagKey.GENRE_NAME]
            if isinstance(raw_value, str):
                return raw_value
            else:
                try:
                    genre_code = int(raw_value)
                    return ID3V1_AND_RIFF_GENRE_CODE_MAP.get(genre_code, None)
                except ValueError:
                    return None
        return None

    def get_track_number(self) -> Optional[int]:
        part = self.file_raw_metadata.get(self.RiffTagKey.TRACK_NUMBER, None)
        if part:
            try:
                return int(part)
            except ValueError:
                return None
        return None

    def update_specific_metadata_without_saving(self, normalized_metadata_value, app_metadata_key: str,):
        if app_metadata_key == AppMetadataKey.TITLE:
            riff_tag_key = self.RiffTagKey.TITLE
        elif app_metadata_key == AppMetadataKey.ARTISTS_NAMES_STR:
            riff_tag_key = self.RiffTagKey.ARTIST_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_NAME:
            riff_tag_key = self.RiffTagKey.ALBUM_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            riff_tag_key = self.RiffTagKey.ALBUM_ARTISTS_NAMES
        elif app_metadata_key == AppMetadataKey.GENRE_NAME:
            riff_tag_key = self.RiffTagKey.GENRE_NAME
        elif app_metadata_key == AppMetadataKey.RATING:
            raise UnsupportedMetadataError("RIFF format does not support ratings")
        elif app_metadata_key == AppMetadataKey.BPM:
            raise UnsupportedMetadataError("RIFF format does not support BPM metadata")
        elif app_metadata_key == AppMetadataKey.LANGUAGE:
            riff_tag_key = self.RiffTagKey.LANGUAGE
        elif app_metadata_key == AppMetadataKey.RELEASE_DATE:
            riff_tag_key = self.RiffTagKey.DATE
        elif app_metadata_key == AppMetadataKey.TRACK_NUMBER:
            riff_tag_key = self.RiffTagKey.TRACK_NUMBER
        else:
            raise UnsupportedMetadataError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        if normalized_metadata_value:
            if riff_tag_key not in self.file_raw_metadata:
                self.file_raw_metadata[riff_tag_key] = [1]
            self.file_raw_metadata[riff_tag_key] = normalized_metadata_value
        elif riff_tag_key in self.file_raw_metadata:
            del self.file_raw_metadata[riff_tag_key]
