from typing import Optional
import struct

from bodzify_api.utils.audio_metadata.MetadataManager import MetadataManager, NormalizedMetadataKeys


class Id3v1Manager(MetadataManager):
    """
    Manages ID3v1 metadata for audio files.

    ID3v1 is a simple metadata format that stores information in a 128-byte block
    at the end of the file. The format is:
    - Bytes 0-2: "TAG" identifier
    - Bytes 3-32: Title (30 chars)
    - Bytes 33-62: Artist (30 chars)
    - Bytes 63-92: Album (30 chars)
    - Bytes 93-96: Year (4 chars)
    - Bytes 97-126: Comment (28 or 30 chars)
    - Byte 127: Genre code (0-255)

    Note: If byte 125 is null and byte 126 is non-null in the comment field,
    then byte 126 is the track number (ID3v1.1 extension).
    """

    # Standard ID3v1 genre codes mapping
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
    }

    def get_raw_metadata(self) -> dict:
        """Read ID3v1 tag from the end of the file."""
        self.audio_file.seek(-128, 2)  # Seek from end
        data = self.audio_file.read(128)
        if not data.startswith(b'TAG'):
            return {}

        # Unpack fixed-length fields
        title = data[3:33].strip(b'\0').decode('latin1', 'replace')
        artist = data[33:63].strip(b'\0').decode('latin1', 'replace')
        album = data[63:93].strip(b'\0').decode('latin1', 'replace')
        year = data[93:97].strip(b'\0').decode('latin1', 'replace')
        comment = data[97:127].strip(b'\0')
        genre = struct.unpack('B', data[127:128])[0]

        # Check for ID3v1.1 track number
        if comment[28] == 0 and comment[29] != 0:
            track = comment[29]
            comment = comment[:28]
        else:
            track = None
            comment = comment[:30]

        comment = comment.decode('latin1', 'replace')

        return {
            'title': [title] if title else [],
            'artist': [artist] if artist else [],
            'album': [album] if album else [],
            'year': [year] if year else [],
            'comment': [comment] if comment else [],
            'genre': [genre] if genre < len(self.GENRE_MAP) else [],
            'track': [track] if track is not None else []
        }

    def get_title(self) -> Optional[str]:
        """Get title from ID3v1 tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none('title')

    def get_artists_names(self) -> Optional[str]:
        """Get artist from ID3v1 tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none('artist')

    def get_album_name(self) -> Optional[str]:
        """Get album name from ID3v1 tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none('album')

    def get_album_artists_name_str(self) -> Optional[str]:
        """ID3v1 doesn't support album artist."""
        return None

    def get_genre_name(self) -> Optional[str]:
        """Get genre name from ID3v1 genre code."""
        if 'genre' in self.file_raw_metadata:
            try:
                genre_code = self.file_raw_metadata['genre'][0]
                return self.GENRE_MAP.get(genre_code, "Other")
            except (IndexError, KeyError):
                return None
        return None

    def get_language(self) -> Optional[str]:
        """ID3v1 doesn't support language tags."""
        return None

    def get_release_date(self) -> Optional[str]:
        """Get release year from ID3v1 tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none('year')

    def get_position_in_album(self) -> Optional[int]:
        """Get track number from ID3v1.1 tag."""
        if 'track' in self.file_raw_metadata:
            try:
                return int(self.file_raw_metadata['track'][0])
            except (ValueError, IndexError):
                return None
        return None

    def get_bitrate(self) -> int:
        """ID3v1 doesn't store bitrate information."""
        return 0

    def get_eventually_normalized_rating_value(self,
                                             normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        """ID3v1 doesn't support ratings."""
        return None

    def update_specific_file_metadata_without_saving(
            self,
            normalized_metadata_value,
            normalized_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        """Update ID3v1 tag field.
        
        Note: This implementation is read-only as modifying ID3v1 tags
        requires careful handling of the fixed-length fields and file seeking.
        """
        raise NotImplementedError("ID3v1 tag modification is not supported")