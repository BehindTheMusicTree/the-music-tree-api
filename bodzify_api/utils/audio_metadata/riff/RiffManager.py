import io
from typing import Optional

from mutagen.wave import WAVE

from bodzify_api.utils.audio_metadata.MetadataManager import MetadataManager, NormalizedMetadataKeys


class RiffManager(MetadataManager):
    # Standard ID3v1/WAV genre codes mapping
    # This is the same mapping used in ID3v1 tags
    GENRE_MAP = {
        0: "Blues", 1: "Classic Rock", 2: "Country", 3: "Dance",
        4: "Disco", 5: "Funk", 6: "Grunge", 7: "Hip-Hop",
        8: "Jazz", 9: "Metal", 10: "New Age", 11: "Oldies",
        12: "Other", 13: "Pop", 14: "R&B", 15: "Rap",
        16: "Reggae", 17: "Rock", 18: "Techno", 19: "Industrial",
        20: "Alternative", 21: "Ska", 22: "Death Metal", 23: "Pranks",
        24: "Soundtrack", 25: "Euro-Techno", 26: "Ambient", 27: "Trip-Hop",
        28: "Vocal", 29: "Jazz+Funk", 30: "Fusion", 31: "Trance",
        32: "Classical", 33: "Instrumental", 34: "Acid", 35: "House",
        36: "Game", 37: "Sound Clip", 38: "Gospel", 39: "Noise",
        40: "Alternative Rock", 41: "Bass", 42: "Soul", 43: "Punk",
        44: "Space", 45: "Meditative", 46: "Instrumental Pop",
        47: "Instrumental Rock", 48: "Ethnic", 49: "Gothic",
        50: "Darkwave", 51: "Techno-Industrial", 52: "Electronic",
        53: "Pop-Folk", 54: "Eurodance", 55: "Dream",
        56: "Southern Rock", 57: "Comedy", 58: "Cult",
        59: "Gangsta", 60: "Top 40", 61: "Christian Rap",
        62: "Pop/Funk", 63: "Jungle", 64: "Native US",
        65: "Cabaret", 66: "New Wave", 67: "Psychadelic",
        68: "Rave", 69: "Showtunes", 70: "Trailer",
        71: "Lo-Fi", 72: "Tribal", 73: "Acid Punk",
        74: "Acid Jazz", 75: "Polka", 76: "Retro",
        77: "Musical", 78: "Rock & Roll", 79: "Hard Rock",
        # More genres can be added as needed
    }
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
                return self.GENRE_MAP.get(genre_code, "Other")
            except (ValueError, TypeError):
                # If the tag contains a string instead of a code, use it directly
                return self.file_raw_metadata[self.RiffTagKeys.GENRE_NAME][0]
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
