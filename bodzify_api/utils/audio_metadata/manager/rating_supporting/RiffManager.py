import io
from typing import cast

from mutagen._file import FileType
from mutagen.wave import WAVE


from ....AudioFile import AudioFile
from ...exceptions import MetadataNotSupportedError
from ...utils.id3v1_genre_code_map import ID3V1_GENRE_CODE_MAP
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadataDict, AppMetadataValue, RawMetadataDict, RawMetadataKey
from ..MetadataManager import AppMetadataKey
from ..rating_supporting.RatingSupportingMetadataManager import RatingSupportingMetadataManager


class RiffManager(RatingSupportingMetadataManager):
    """
    Manages RIFF metadata for WAV audio files.

    Implementation Note:
    While mutagen is used for reading WAV metadata, it does not support writing RIFF metadata. This is a known
    limitation of the library, which only provides read-only access to WAVE files' metadata through its WAVE class.
    Therefore, this manager implements its own RIFF metadata writing functionality by directly manipulating the file's
    INFO chunk according to the RIFF specification.

    RIFF Format:
    RIFF (Resource Interchange File Format) is the standard metadata format for WAV files. The INFO chunk in RIFF/WAV
    files uses standardized 4-character codes (FourCC) like INAM(Title), IART(Artist) or ICMT(Comments).

    These codes are defined in RiffTagKey and are part of the standard RIFF specification. Each tag in the INFO chunk
    follows the format:
    - FourCC (4 chars): Identifies the metadata field (e.g., 'INAM' for title)
    - Size (4 bytes): Length of the data in bytes
    - Data (UTF-8): The actual metadata content
    - Padding: If needed for word alignment (2 bytes)

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

    Note: This manager is the preferred way to handle WAV metadata, as it uses the format's native metadata system
    rather than non-standard alternatives like ID3v2 tags. The custom implementation ensures proper handling of RIFF
    chunk structures, maintaining word alignment and size fields according to the specification.
    """

    class RiffTagKey(RawMetadataKey):
        # Standard
        TITLE = 'INAM'
        ARTIST_NAME = 'IART'
        ALBUM_NAME = 'IPRD'
        GENRE_NAME_OR_ID3V1_CODE = 'IGNR'
        DATE = 'ICRD'  # Creation/Release date
        TRACK_NUMBER = 'IPRT'

        # Non-standard
        ALBUM_ARTISTS_NAMES = 'IAAR'
        LANGUAGE = 'ILNG'
        RATING = 'IRTD'
        COMMENTS = 'ICMT'
        ENGINEER = 'IENG'  # Engineer who worked on the track
        SOFTWARE = 'ISFT'  # Software used to create the file
        COPYRIGHT = 'ICOP'
        TECHNICIAN = 'ITCH'  # Technician who worked on the track

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: None | int = None):
        metadata_keys_direct_map_read = {
            AppMetadataKey.TITLE: self.RiffTagKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES: self.RiffTagKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.RiffTagKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: self.RiffTagKey.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: None,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            # AppMetadataKey.TRACK_NUMBER: None,
        }
        metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None] = {
            AppMetadataKey.TITLE: self.RiffTagKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES: self.RiffTagKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.RiffTagKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: self.RiffTagKey.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: None,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            # AppMetadataKey.TRACK_NUMBER: self.RiffTagKey.TRACK_NUMBER,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_100_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_mutagen_metadata(self) -> FileType:
        """
        Extract RIFF metadata by directly reading the INFO chunk.
        WAVE/RIFF files are structured as:
        'RIFF' + size + 'WAVE' + chunks, where each chunk is:
        FourCC + size + data
        We look for the LIST chunk containing INFO data.
        """
        self.audio_file.seek(0)
        file_data = self.audio_file.read()
        wave = WAVE(io.BytesIO(file_data))

        # Store INFO chunk data in a custom attribute
        info_tags: dict[str, str] = {}

        # Parse RIFF chunks directly since mutagen doesn't expose all metadata
        pos = 0
        size = len(file_data)
        while pos < size - 8:  # Need at least 8 bytes for chunk header
            if file_data[pos:pos+4] == b'LIST' and file_data[pos+8:pos+12] == b'INFO':
                info_size = int.from_bytes(file_data[pos+4:pos+8], 'little')
                info_data = file_data[pos+12:pos+12+info_size-4]  # -4 for 'INFO'

                # Parse INFO chunk tags
                tag_pos = 0
                while tag_pos < len(info_data) - 8:
                    tag_id = info_data[tag_pos:tag_pos+4].decode('ascii')
                    tag_size = int.from_bytes(info_data[tag_pos+4:tag_pos+8], 'little')
                    tag_data = info_data[tag_pos+8:tag_pos+8+tag_size].decode('utf-8').rstrip('\x00')

                    # Store in our custom dict
                    info_tags[tag_id] = tag_data

                    # Move to next tag (aligned to word boundary)
                    tag_pos += 8 + ((tag_size + 1) & ~1)
                break
            pos += 1

        # Store the parsed INFO tags as a custom attribute
        setattr(wave, 'info', info_tags)
        return wave

    def _convert_mutagen_metadata_to_dict_with_potential_duplicate_keys_and_multi_values(self) -> RawMetadataDict:
        """
        Convert RIFF metadata to dictionary.
        Extracts tags from our custom info_tags attribute which contains
        the directly parsed INFO chunk data.
        """
        raw_mutagen_metadata_wav: WAVE = self.raw_mutagen_metadata  # type: ignore
        raw_metadata_dict: dict = {}

        # Get metadata from our custom info which contains the directly parsed INFO chunk
        if hasattr(raw_mutagen_metadata_wav, 'info'):
            info_tags = getattr(raw_mutagen_metadata_wav, 'info')
            for key, value in info_tags.items():
                if key in self.RiffTagKey:
                    raw_metadata_dict[key] = value

        return raw_metadata_dict

    def _get_raw_mutagen_metadata_rating_by_traktor_or_not(self) -> tuple[int | None, bool]:
        if not self.raw_mutagen_metadata.info or self.RiffTagKey.RATING not in self.raw_mutagen_metadata.info:
            return None, False

        raw_rating = self.raw_mutagen_metadata.info[self.RiffTagKey.RATING]
        if raw_rating is None:
            return None, False
        try:
            return int(raw_rating), False
        except ValueError:
            return None, False

    def _get_undirectly_mapped_metadata_value_other_than_rating(self, key: AppMetadataKey) -> AppMetadataValue:
        if key == AppMetadataKey.GENRE_NAME:
            genre_name = self._get_genre_name()
            return [genre_name] if genre_name else None
        else:
            raise MetadataNotSupportedError(f'Metadata key not handled: {key}')

    def _get_genre_name(self) -> str | None:
        """
        The IGNR tag in RIFF files typically contains a genre code
        that corresponds to the ID3v1 genre list. This method converts
        the code to a human-readable genre name.
        """
        if self.RiffTagKey.GENRE_NAME_OR_ID3V1_CODE in self.raw_mutagen_metadata:
            raw_value = self.raw_mutagen_metadata[self.RiffTagKey.GENRE_NAME_OR_ID3V1_CODE]
            if isinstance(raw_value, str):
                return raw_value
            else:
                try:
                    genre_code = int(raw_value)
                    return ID3V1_GENRE_CODE_MAP.get(genre_code, None)
                except ValueError:
                    return None
        return None

    def _get_track_number(self) -> int | None:
        part = self.raw_mutagen_metadata.get(self.RiffTagKey.TRACK_NUMBER, None)
        if part:
            try:
                return int(part)
            except ValueError:
                return None
        return None

    def _update_formatted_value_in_raw_mutagen_metadata(
            self, raw_metadata_key: RawMetadataKey, app_metadata_value: AppMetadataValue):
        """
        Update a single metadata field in the RIFF INFO chunk.
        Since mutagen doesn't support writing RIFF metadata, we implement our own writer.
        First removes any existing tag with the same key to prevent multi-values.
        """
        # Read the entire file
        self.audio_file.seek(0)
        file_data = bytearray(self.audio_file.read())

        # Find the LIST INFO chunk
        pos = 0
        size = len(file_data)
        info_chunk_start = 0
        info_chunk_size = 0
        has_info_chunk = False

        while pos < size - 8:  # Need at least 8 bytes for chunk header
            if file_data[pos:pos+4] == b'LIST' and file_data[pos+8:pos+12] == b'INFO':
                info_chunk_start = pos
                info_chunk_size = int.from_bytes(file_data[pos+4:pos+8], 'little')
                has_info_chunk = True
                break
            pos += 1

        # Remove existing tag if present
        if has_info_chunk:
            info_data_start = info_chunk_start + 12  # After LIST+size+INFO
            info_data_end = info_data_start + info_chunk_size - 4  # -4 for 'INFO'
            tag_pos = info_data_start

            while tag_pos < info_data_end - 8:  # Need at least 8 bytes for tag header
                tag_id = file_data[tag_pos:tag_pos+4].decode('ascii')
                tag_size = int.from_bytes(file_data[tag_pos+4:tag_pos+8], 'little')
                total_tag_size = 8 + ((tag_size + 1) & ~1)  # Include header and padding

                if tag_id == raw_metadata_key:
                    # Remove the tag by shifting remaining data left
                    file_data[tag_pos: tag_pos + info_chunk_size - total_tag_size] = file_data[tag_pos +
                                                                                               total_tag_size: tag_pos + info_chunk_size]
                    # Update chunk sizes
                    info_chunk_size -= total_tag_size
                    file_data[info_chunk_start+4:info_chunk_start+8] = info_chunk_size.to_bytes(4, 'little')
                    riff_size = int.from_bytes(file_data[4:8], 'little')
                    file_data[4:8] = (riff_size - total_tag_size).to_bytes(4, 'little')
                    break

                tag_pos += total_tag_size

        # Create new INFO chunk if none exists
        if not has_info_chunk:
            # Find RIFF header size
            riff_size = int.from_bytes(file_data[4:8], 'little')
            # Insert after WAVE header
            info_chunk_start = 12  # After RIFF+size+WAVE
            info_chunk_size = 4  # Initial size just for 'INFO'
            # Insert empty LIST INFO chunk
            file_data[4:8] = (riff_size + info_chunk_size + 8).to_bytes(4, 'little')  # Update RIFF size
            file_data[info_chunk_start:info_chunk_start] = b'LIST' + info_chunk_size.to_bytes(4, 'little') + b'INFO'

        # Convert value to string if it's a list
        if isinstance(app_metadata_value, list):
            value = app_metadata_value[0] if app_metadata_value else ""
        else:
            value = app_metadata_value if app_metadata_value is not None else ""

        # Convert to bytes, ensuring UTF-8 encoding
        value_bytes = str(value).encode('utf-8')
        # Add null terminator and pad to even length
        value_bytes += b'\x00'
        if len(value_bytes) % 2:
            value_bytes += b'\x00'

        # Create tag data
        tag_data = raw_metadata_key.encode('ascii') + len(value_bytes).to_bytes(4, 'little') + value_bytes

        # Insert at end of INFO chunk
        insert_pos = info_chunk_start + 12 + info_chunk_size - 4  # After LIST+size+INFO
        file_data[insert_pos:insert_pos] = tag_data

        # Update chunk sizes
        info_chunk_size += len(tag_data)
        file_data[info_chunk_start+4:info_chunk_start+8] = info_chunk_size.to_bytes(4, 'little')
        riff_size = int.from_bytes(file_data[4:8], 'little')
        file_data[4:8] = (riff_size + len(tag_data)).to_bytes(4, 'little')

        # Write back to file
        self.audio_file.seek(0)
        self.audio_file.write(file_data)

        # Update our cached metadata
        if not hasattr(self.raw_mutagen_metadata, 'info'):
            setattr(self.raw_mutagen_metadata, 'info', {})
        info_dict = getattr(self.raw_mutagen_metadata, 'info')
        if isinstance(info_dict, dict):
            info_dict[raw_metadata_key] = str(value)

    def update_bulk(self, app_metadata_dict: AppMetadataDict):
        """
        Update multiple metadata fields in the RIFF INFO chunk.
        Since mutagen doesn't support writing RIFF metadata, we implement our own writer.
        """

        if not self.metadata_keys_direct_map_write:
            raise MetadataNotSupportedError("No writable metadata keys found")

        # Read the entire file
        self.audio_file.seek(0)
        file_data = bytearray(self.audio_file.read())

        # Find the LIST INFO chunk
        pos = 0
        size = len(file_data)
        info_chunk_start = 0
        info_chunk_size = 0
        has_info_chunk = False

        while pos < size - 8:  # Need at least 8 bytes for chunk header
            if file_data[pos:pos+4] == b'LIST' and file_data[pos+8:pos+12] == b'INFO':
                info_chunk_start = pos
                info_chunk_size = int.from_bytes(file_data[pos+4:pos+8], 'little')
                has_info_chunk = True
                break
            pos += 1

        # Create new INFO chunk if none exists
        if not has_info_chunk:
            # Find RIFF header size
            riff_size = int.from_bytes(file_data[4:8], 'little')
            # Insert after WAVE header
            info_chunk_start = 12  # After RIFF+size+WAVE
            info_chunk_size = 4  # Initial size just for 'INFO'
            # Insert empty LIST INFO chunk
            file_data[4:8] = (riff_size + info_chunk_size + 8).to_bytes(4, 'little')  # Update RIFF size
            file_data[info_chunk_start:info_chunk_start] = b'LIST' + info_chunk_size.to_bytes(4, 'little') + b'INFO'

        # Remove existing tags and write new ones
        for app_key, value in app_metadata_dict.items():
            if value is None or value == "":
                continue

            # Get corresponding RIFF tag from the guaranteed-to-exist map
            riff_key = self.metadata_keys_direct_map_write.get(app_key)
            if not riff_key:
                if app_key == AppMetadataKey.GENRE_NAME:
                    riff_key = self.RiffTagKey.GENRE_NAME_OR_ID3V1_CODE
                    value = self._get_genre_code(str(value))
                elif app_key == AppMetadataKey.RATING:
                    riff_key = self.RiffTagKey.RATING
                    app_rating = cast(int, value)
                    value = self._convert_normalized_rating_to_file_rating(app_rating)
                else:
                    raise MetadataNotSupportedError(f"Metadata key not handled: {app_key}")

            # Remove existing tag if present
            if has_info_chunk:
                info_data_start = info_chunk_start + 12  # After LIST+size+INFO
                info_data_end = info_data_start + info_chunk_size - 4  # -4 for 'INFO'
                tag_pos = info_data_start

                while tag_pos < info_data_end - 8:  # Need at least 8 bytes for tag header
                    tag_id = file_data[tag_pos:tag_pos+4].decode('ascii')
                    tag_size = int.from_bytes(file_data[tag_pos+4:tag_pos+8], 'little')
                    total_tag_size = 8 + ((tag_size + 1) & ~1)  # Include header and padding

                    if tag_id == riff_key:
                        # Remove the tag by shifting remaining data left
                        file_data[tag_pos: tag_pos + info_chunk_size - total_tag_size] = file_data[tag_pos +
                                                                                                   total_tag_size: tag_pos + info_chunk_size]
                        # Update chunk sizes
                        info_chunk_size -= total_tag_size
                        file_data[info_chunk_start+4:info_chunk_start+8] = info_chunk_size.to_bytes(4, 'little')
                        riff_size = int.from_bytes(file_data[4:8], 'little')
                        file_data[4:8] = (riff_size - total_tag_size).to_bytes(4, 'little')
                        break

                    tag_pos += total_tag_size

            # Convert value to string if it's a list
            if isinstance(value, list):
                value = value[0] if value else ""

            # Convert to bytes, ensuring UTF-8 encoding
            value_bytes = str(value).encode('utf-8')
            # Add null terminator and pad to even length
            value_bytes += b'\x00'
            if len(value_bytes) % 2:
                value_bytes += b'\x00'

            # Create tag data
            tag_data = riff_key.encode('ascii') + len(value_bytes).to_bytes(4, 'little') + value_bytes

            # Insert at end of INFO chunk
            insert_pos = info_chunk_start + 12 + info_chunk_size - 4  # After LIST+size+INFO
            file_data[insert_pos:insert_pos] = tag_data

            # Update chunk sizes
            info_chunk_size += len(tag_data)
            file_data[info_chunk_start+4:info_chunk_start+8] = info_chunk_size.to_bytes(4, 'little')
            riff_size = int.from_bytes(file_data[4:8], 'little')
            file_data[4:8] = (riff_size + len(tag_data)).to_bytes(4, 'little')

        # Write back to file
        self.audio_file.seek(0)
        self.audio_file.write(file_data)

    def _get_genre_code(self, genre_name: str) -> int | None:
        for code, name in ID3V1_GENRE_CODE_MAP.items():
            if name == genre_name:
                return code
        return None
