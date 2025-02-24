import io
from typing import Dict, Optional

from mutagen.wave import WAVE

from bodzify_api.utils.audio_metadata.manager.MetadataManager import MetadataManager, AppMetadataKey
from bodzify_api.utils.audio_metadata.utils.id3v1_and_riff_genre_code_map import ID3V1_AND_RIFF_GENRE_CODE_MAP
from bodzify_api.utils.audio_metadata.exceptions import UnsupportedMetadataError


class RiffManager(MetadataManager):
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

    class RiffTagKeys:
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

    def extract_raw_metadata_dict(self) -> Dict:
        self.audio_file.seek(0)
        wave_file = WAVE(io.BytesIO(self.audio_file.read()))
        return {
            'info': wave_file.info.__dict__,
            'tags': wave_file.tags if wave_file.tags else {},
        }

    def get_eventually_normalized_rating_from_file(
            self, normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        raise UnsupportedMetadataError("RIFF format does not support ratings")

    def get_title(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.RiffTagKeys.TITLE)

    def get_artists_names(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.RiffTagKeys.ARTIST_NAME)

    def get_album_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.RiffTagKeys.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        album_artists_name_str_raw = self._get_first_value_str_if_exists_in_raw_metadata_or_none(
            key=self.RiffTagKeys.ALBUM_ARTISTS_NAMES)
        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> Optional[str]:
        """Get genre name from IGNR tag.

        The IGNR tag in RIFF files typically contains a genre code
        that corresponds to the ID3v1 genre list. This method converts
        the code to a human-readable genre name.

        Returns:
            str: Genre name if available, empty string if not found
        """
        if self.RiffTagKeys.GENRE_NAME in self.file_raw_metadata:
            try:
                # Try to get genre code and convert to name
                genre_code = int(self.file_raw_metadata[self.RiffTagKeys.GENRE_NAME][0])
                return ID3V1_AND_RIFF_GENRE_CODE_MAP.get(genre_code, "Other")
            except (ValueError, TypeError):
                # If the tag contains a string instead of a code, use it directly
                return self.file_raw_metadata[self.RiffTagKeys.GENRE_NAME][0]
        return ""

    def get_language(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.RiffTagKeys.LANGUAGE)

    def get_release_date_str(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.RiffTagKeys.DATE)

    def get_track_number(self) -> Optional[int]:
        part = self._get_first_value_str_if_exists_in_raw_metadata_or_none(key=self.RiffTagKeys.TRACK_NUMBER)
        if part:
            try:
                return int(part)
            except ValueError:
                return None
        return None

    def update_specific_metadata_without_saving(
            self,
            normalized_metadata_value,
            app_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        if app_metadata_key == AppMetadataKey.TITLE:
            riff_tag_key = self.RiffTagKeys.TITLE
        elif app_metadata_key == AppMetadataKey.ARTISTS_NAMES_STR:
            riff_tag_key = self.RiffTagKeys.ARTIST_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_NAME:
            riff_tag_key = self.RiffTagKeys.ALBUM_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            riff_tag_key = self.RiffTagKeys.ALBUM_ARTISTS_NAMES
        elif app_metadata_key == AppMetadataKey.GENRE_NAME:
            riff_tag_key = self.RiffTagKeys.GENRE_NAME
        elif app_metadata_key == AppMetadataKey.RATING:
            raise UnsupportedMetadataError("RIFF format does not support ratings")
        elif app_metadata_key == AppMetadataKey.BPM:
            raise UnsupportedMetadataError("RIFF format does not support BPM metadata")
        elif app_metadata_key == AppMetadataKey.LANGUAGE:
            riff_tag_key = self.RiffTagKeys.LANGUAGE
        elif app_metadata_key == AppMetadataKey.RELEASE_DATE:
            riff_tag_key = self.RiffTagKeys.DATE
        elif app_metadata_key == AppMetadataKey.TRACK_NUMBER:
            riff_tag_key = self.RiffTagKeys.TRACK_NUMBER
        else:
            raise UnsupportedMetadataError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        if normalized_metadata_value:
            if riff_tag_key not in self.file_raw_metadata:
                self.file_raw_metadata[riff_tag_key] = [1]
            self.file_raw_metadata[riff_tag_key] = normalized_metadata_value
        elif riff_tag_key in self.file_raw_metadata:
            del self.file_raw_metadata[riff_tag_key]
