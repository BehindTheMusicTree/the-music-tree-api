import io
from typing import Optional

from mutagen.wave import WAVE

from bodzify_api.utils.audio_metadata.MetadataManager import MetadataManager, NormalizedMetadataKeys


class RiffManager(MetadataManager):
    """
    Manages RIFF metadata for WAV audio files.

    RIFF (Resource Interchange File Format) is used to store metadata in WAV files.
    WAV files use the INFO chunk for storing metadata, with standardized four-character codes (FourCC).
    Common INFO chunk fields include:
    - INAM: Title
    - IART: Artist
    - IPRD: Album
    - IGNR: Genre
    - ICMT: Comments
    - ICRD: Creation date
    - IENG: Engineer
    - ISFT: Software
    - ICOP: Copyright
    - ITCH: Technician
    - IPRT: Part number (track number)
    """

    class RiffTagKeys:
        TITLE = 'INAM'
        ARTIST_NAME = 'IART'
        ALBUM_NAME = 'IPRD'
        ALBUM_ARTISTS_NAMES = 'IAAR'  # Non-standard but commonly used
        GENRE_NAME = 'IGNR'
        LANGUAGE = 'ILNG'  # Non-standard but commonly used
        RELEASE_DATE = 'ICRD'  # Creation/Release date
        PART = 'IPRT'  # Part number (track number)

    def get_raw_metadata(self) -> dict:
        """Get raw metadata from WAV file."""
        self.audio_file.seek(0)
        wave_file = WAVE(io.BytesIO(self.audio_file.read()))
        return {
            'info': wave_file.info.__dict__,
            'tags': wave_file.tags if wave_file.tags else {},
        }

    def get_eventually_normalized_rating_value(self,
                                               normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        """WAV files don't typically support ratings, return None."""
        return None

    def get_title(self) -> Optional[str]:
        """Get title from INAM tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.RiffTagKeys.TITLE)

    def get_artists_names(self) -> Optional[str]:
        """Get artist from IART tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.RiffTagKeys.ARTIST_NAME)

    def get_album_name(self) -> Optional[str]:
        """Get album name from IPRD tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.RiffTagKeys.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        """Get album artist from IAAR tag."""
        album_artists_name_str_raw = self._get_first_value_str_if_exists_in_file_metadata_or_none(
            key=self.RiffTagKeys.ALBUM_ARTISTS_NAMES)
        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> Optional[str]:
        """Get genre from IGNR tag."""
        if self.RiffTagKeys.GENRE_NAME in self.file_raw_metadata:
            return self.file_raw_metadata[self.RiffTagKeys.GENRE_NAME][0]
        else:
            return ""

    def get_language(self) -> Optional[str]:
        """Get language from ILNG tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.RiffTagKeys.LANGUAGE)

    def get_release_date(self) -> Optional[str]:
        """Get release date from ICRD tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.RiffTagKeys.RELEASE_DATE)

    def get_position_in_album(self) -> Optional[int]:
        """Get track number from IPRT (Part) tag.
        
        Returns:
            Optional[int]: Track number if available, None otherwise
        """
        part = self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.RiffTagKeys.PART)
        if part:
            try:
                return int(part)
            except ValueError:
                return None
        return None

    def get_bitrate(self) -> int:
        """Get bitrate from WAV info."""
        return self.file_raw_metadata['info']['bitrate'] // 1000

    def update_specific_file_metadata_without_saving(
            self,
            normalized_metadata_value,
            normalized_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        """Update specific metadata field in WAV file."""
        if normalized_metadata_key == NormalizedMetadataKeys.TITLE:
            riff_tag_key = self.RiffTagKeys.TITLE
        elif normalized_metadata_key == NormalizedMetadataKeys.ARTISTS_NAMES_STR:
            riff_tag_key = self.RiffTagKeys.ARTIST_NAME
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_NAME:
            riff_tag_key = self.RiffTagKeys.ALBUM_NAME
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES_STR:
            riff_tag_key = self.RiffTagKeys.ALBUM_ARTISTS_NAMES
        elif normalized_metadata_key == NormalizedMetadataKeys.GENRE_NAME:
            riff_tag_key = self.RiffTagKeys.GENRE_NAME
        elif normalized_metadata_key == NormalizedMetadataKeys.RATING:
            # WAV files don't support ratings
            return
        elif normalized_metadata_key == NormalizedMetadataKeys.LANGUAGE:
            riff_tag_key = self.RiffTagKeys.LANGUAGE
        elif normalized_metadata_key == NormalizedMetadataKeys.RELEASE_DATE:
            riff_tag_key = self.RiffTagKeys.RELEASE_DATE
        elif normalized_metadata_key == NormalizedMetadataKeys.POSITION_IN_ALBUM:
            riff_tag_key = self.RiffTagKeys.PART
        else:
            raise KeyError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        if normalized_metadata_value:
            if riff_tag_key not in self.file_raw_metadata:
                self.file_raw_metadata[riff_tag_key] = [1]
            self.file_raw_metadata[riff_tag_key] = normalized_metadata_value
        elif riff_tag_key in self.file_raw_metadata:
            del self.file_raw_metadata[riff_tag_key]