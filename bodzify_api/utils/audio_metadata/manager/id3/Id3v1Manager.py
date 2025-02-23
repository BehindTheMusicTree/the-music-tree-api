from typing import Optional
import struct

from bodzify_api.utils.audio_metadata.manager.MetadataManager import MetadataManager, NormalizedMetadataKeys
from bodzify_api.utils.audio_metadata.constants import ID3V1_AND_RIFF_GENRE_MAP
from bodzify_api.utils.audio_metadata.exceptions import UnsupportedMetadataError


class Id3v1Manager(MetadataManager):
    """
    Manages ID3v1 metadata for audio files.

    ID3v1 is a simple, legacy metadata format with significant limitations:
    - Fixed 128-byte block at end of file
    - No Unicode support (Latin-1 only)
    - Limited field lengths (30 chars)
    - No support for:
        - Album artist
        - BPM
        - Ratings
        - Language
        - Custom genres
        - Multiple genres
        - Multiple artists
    - Read-only (modification not safe)

    Format Structure:
    - Bytes 0-2: "TAG" identifier
    - Bytes 3-32: Title (30 chars)
    - Bytes 33-62: Artist (30 chars)
    - Bytes 63-92: Album (30 chars)
    - Bytes 93-96: Release year (4 chars)
    - Bytes 97-126: Comment (28 chars in ID3v1.1, 30 chars in ID3v1)
    - Byte 125: Always 0 in ID3v1.1 to indicate track number presence
    - Byte 126: Track number in ID3v1.1 (1-255, 0 = not set)
    - Byte 127: Genre code (0-255)

    Note: ID3v1.1 extends ID3v1 by using the last two bytes of the comment
    field to store the track number. If byte 125 is 0 and byte 126 is not 0,
    then byte 126 contains the track number (1-255).
    """

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
            track = str(comment[29])  # Convert track number byte to string
            comment = comment[:28]
        else:
            track = None
            comment = comment[:30]

        comment = comment.decode('latin1', 'replace')

        metadata = {}

        if title:
            metadata[NormalizedMetadataKeys.TITLE] = [title]
        if artist:
            metadata[NormalizedMetadataKeys.ARTISTS_NAMES_STR] = [artist]
        if album:
            metadata[NormalizedMetadataKeys.ALBUM_NAME] = [album]
        if year:
            metadata[NormalizedMetadataKeys.RELEASE_DATE] = [year]
        # Comments are not part of normalized metadata
        if genre < len(ID3V1_AND_RIFF_GENRE_MAP):
            metadata[NormalizedMetadataKeys.GENRE_NAME] = [genre]
        if track and track != '0':
            metadata[NormalizedMetadataKeys.POSITION_IN_ALBUM] = [track]

        return metadata

    def get_title(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(NormalizedMetadataKeys.TITLE)

    def get_artists_names(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(NormalizedMetadataKeys.ARTISTS_NAMES_STR)

    def get_album_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(NormalizedMetadataKeys.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        """Get album artist.

        Raises:
            UnsupportedMetadataError: ID3v1 does not support album artist
        """
        raise UnsupportedMetadataError("ID3v1 format does not support album artist")

    def get_genre_name(self) -> Optional[str]:
        """Get genre name from ID3v1 genre code."""
        if NormalizedMetadataKeys.GENRE_NAME in self.file_raw_metadata:
            try:
                genre_code = self.file_raw_metadata[NormalizedMetadataKeys.GENRE_NAME][0]
                return ID3V1_AND_RIFF_GENRE_MAP.get(genre_code, "Other")
            except (IndexError, KeyError):
                return None
        return None

    def get_language(self) -> Optional[str]:
        """Get language.

        Raises:
            UnsupportedMetadataError: ID3v1 does not support language tags
        """
        raise UnsupportedMetadataError("ID3v1 format does not support language tags")

    def get_release_date(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(NormalizedMetadataKeys.RELEASE_DATE)

    def get_position_in_album(self) -> Optional[int]:
        if NormalizedMetadataKeys.POSITION_IN_ALBUM in self.file_raw_metadata:
            try:
                return int(self.file_raw_metadata[NormalizedMetadataKeys.POSITION_IN_ALBUM][0])
            except (ValueError, IndexError):
                return None
        return None

    def get_bpm(self) -> Optional[float]:
        """Get BPM (Beats Per Minute).

        Raises:
            UnsupportedMetadataError: ID3v1 does not support BPM metadata
        """
        raise UnsupportedMetadataError("ID3v1 format does not support BPM metadata")

    def get_eventually_normalized_rating_value(self,
                                               normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        """Get rating.

        Raises:
            UnsupportedMetadataError: ID3v1 does not support ratings
        """
        raise UnsupportedMetadataError("ID3v1 format does not support ratings")

    def update_specific_file_metadata_without_saving(
            self,
            normalized_metadata_value,
            normalized_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        """Update ID3v1 tag field.

        Raises:
            UnsupportedMetadataError: ID3v1 is read-only due to fixed-length fields
        """
        raise UnsupportedMetadataError(
            "ID3v1 tag modification is not supported (fixed-length format)")