

from dataclasses import dataclass
import struct
from typing import Any, Dict

from bodzify_api.utils.audio_metadata.exceptions import UnsupportedMetadataError
from bodzify_api.utils.audio_metadata.manager.id3v1.Id3v1RawMetadataKey import Id3v1RawMetadataKey


class Id3v1RawMetadata:
    """
    A custom file-like object for ID3v1 tags, providing a consistent interface similar to mutagen.

    This class encapsulates the ID3v1 128-byte structure and provides a clean interface for accessing
    the tag data. It's read-only by design, following ID3v1's limitations.
    """

    @dataclass
    class Id3v1Tag:
        title: str = ''
        artists_names_str: str = ''
        album_name: str = ''
        year: str = ''
        comment: str = ''
        track_number: int | None = None
        genre_code: int = 255  # 255 is undefined genre

    def __init__(self, fileobj: Any):
        self.fileobj = fileobj
        self.tags: Dict[str, list[str]] | None = None
        self._load_tags()

    def _load_tags(self) -> None:
        self.fileobj.seek(-128, 2)  # Seek from end
        data = self.fileobj.read(128)

        if not data.startswith(b'TAG'):
            self.tags = None
            return

        # Parse the fixed structure into our tag object
        tag = self.Id3v1Tag(
            title=data[3:33].strip(b'\0').decode('latin1', 'replace'),
            artists_names_str=data[33:63].strip(b'\0').decode('latin1', 'replace'),
            album_name=data[63:93].strip(b'\0').decode('latin1', 'replace'),
            year=data[93:97].strip(b'\0').decode('latin1', 'replace'),
            genre_code=struct.unpack('B', data[127:128])[0]
        )

        # Handle ID3v1.1 track number in comment field
        comment = data[97:127].strip(b'\0')
        if comment[28] == 0 and comment[29] != 0:
            tag.track_number = comment[29]
            tag.comment = comment[:28].decode('latin1', 'replace')
        else:
            tag.comment = comment[:30].decode('latin1', 'replace')

        # Convert to dictionary format similar to other metadata managers
        self.tags = {}
        if tag.title:
            self.tags[Id3v1RawMetadataKey.TITLE.value] = [tag.title]
        if tag.artists_names_str:
            self.tags[Id3v1RawMetadataKey.ARTISTS_NAMES_STR.value] = [tag.artists_names_str]
        if tag.album_name:
            self.tags[Id3v1RawMetadataKey.ALBUM_NAME.value] = [tag.album_name]
        if tag.year:
            self.tags[Id3v1RawMetadataKey.YEAR.value] = [tag.year]
        if tag.genre_code:
            self.tags[Id3v1RawMetadataKey.GENRE_CODE.value] = [str(tag.genre_code)]
        if tag.track_number and tag.track_number != 0:
            self.tags[Id3v1RawMetadataKey.TRACK_NUMBER.value] = [str(tag.track_number)]
        if tag.comment:
            self.tags[Id3v1RawMetadataKey.COMMENT.value] = [tag.comment]

    def save(self) -> None:
        """Placeholder for save operation - ID3v1 is read-only."""
        raise UnsupportedMetadataError()
