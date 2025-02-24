
from typing import Dict, Optional, cast
import struct

from ..utils.AudioFile import AudioFile
from ..utils.types import AppMetadataValue, RawMetadataKey
from ..exceptions import UnsupportedMetadataError
from ..utils.AppMetadataKey import AppMetadataKey
from ..utils.id3v1_and_riff_genre_code_map import ID3V1_AND_RIFF_GENRE_CODE_MAP
from .MetadataManager import MetadataManager


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
        ...
    - Read-only (modification not safe). ID3v1 tags have a fixed size of 128 bytes. Each field within the tag has a 
    specific length (e.g., 30 bytes for title, artist, and album). This fixed size can make it challenging to modify the 
    tags without potentially corrupting the file or losing data.

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

    Note 2: The genre code is an index into a predefined list of genres. 
    """

    class Id3v1RawMetadataKey(RawMetadataKey):
        TITLE = AppMetadataKey.TITLE.value
        ARTISTS_NAMES_STR = AppMetadataKey.ARTISTS_NAMES_STR.value
        ALBUM_NAME = AppMetadataKey.ALBUM_NAME.value
        GENRE_NAME = AppMetadataKey.GENRE_NAME.value

    def __init__(self, audio_file: AudioFile):
        metadata_keys_diract_map: Dict = {
            AppMetadataKey.TITLE: self.Id3v1RawMetadataKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.Id3v1RawMetadataKey.ARTISTS_NAMES_STR,
            AppMetadataKey.ALBUM_NAME: self.Id3v1RawMetadataKey.ALBUM_NAME,
            AppMetadataKey.GENRE_NAME: self.Id3v1RawMetadataKey.GENRE_NAME,
        }
        super().__init__(audio_file=audio_file, metadata_keys_direct_map=metadata_keys_diract_map)

    def extract_raw_metadata_dict(self) -> Dict:
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
            metadata[AppMetadataKey.TITLE.value] = [title]
        if artist:
            metadata[AppMetadataKey.ARTISTS_NAMES_STR.value] = [artist]
        if album:
            metadata[AppMetadataKey.ALBUM_NAME.value] = [album]
        if year:
            metadata[AppMetadataKey.RELEASE_DATE.value] = [year]
        # Comments are not part of normalized metadata
        if genre < len(ID3V1_AND_RIFF_GENRE_CODE_MAP):
            metadata[AppMetadataKey.GENRE_NAME.value] = [genre]
        if track and track != '0':
            metadata[AppMetadataKey.TRACK_NUMBER.value] = [track]

        return metadata

    def _get_str_metadata_value(self, key: AppMetadataKey) -> Optional[str]:
        if key in self.file_raw_metadata:
            return cast(str, self.file_raw_metadata[key.value])
        return None

    def _get_int_metadata_value(self, key: AppMetadataKey) -> Optional[int]:
        if key in self.file_raw_metadata:
            return cast(int, self.file_raw_metadata[key.value])
        return None

    def get_title(self) -> Optional[str]:
        return self._get_str_metadata_value(AppMetadataKey.TITLE)

    def get_artists_names(self) -> Optional[str]:
        return self._get_str_metadata_value(AppMetadataKey.ARTISTS_NAMES_STR)

    def get_album_name(self) -> Optional[str]:
        return self._get_str_metadata_value(AppMetadataKey.ALBUM_NAME)

    def get_genre_name(self) -> Optional[str]:
        genre_code = self._get_int_metadata_value(AppMetadataKey.GENRE_NAME)
        if not genre_code:
            return None
        if not 0 <= genre_code < len(ID3V1_AND_RIFF_GENRE_CODE_MAP):
            return None
        return ID3V1_AND_RIFF_GENRE_CODE_MAP[genre_code]

    def get_release_date_str(self) -> Optional[str]:
        return self._get_str_metadata_value(AppMetadataKey.RELEASE_DATE)

    def get_track_number(self) -> Optional[int]:
        return self._get_int_metadata_value(AppMetadataKey.TRACK_NUMBER)

    def update_specific_metadata_without_saving(
            self, app_metadata_value: AppMetadataValue, app_metadata_key: AppMetadataKey,
            normalized_rating_max_value: Optional[int] = None):
        raise UnsupportedMetadataError(
            "ID3v1 tag modification is not supported (fixed-length format)")
