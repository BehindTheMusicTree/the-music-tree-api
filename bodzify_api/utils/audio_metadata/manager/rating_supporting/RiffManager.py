import io

from mutagen._file import FileType
from mutagen.wave import WAVE

from ....AudioFile import AudioFile
from ...exceptions import UnsupportedMetadataError
from ...utils.id3v1_and_riff_genre_code_map import ID3V1_AND_RIFF_GENRE_CODE_MAP
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadataValue, RawMetadataDict, RawMetadataKey
from ..MetadataManager import AppMetadataKey
from ..rating_supporting.RatingSupportingMetadataManager import RatingSupportingMetadataManager


class RiffManager(RatingSupportingMetadataManager):
    """
    Manages RIFF metadata for WAV audio files.

    RIFF (Resource Interchange File Format) is the standard metadata format for WAV files.

    The INFO chunk in RIFF/WAV files uses standardized 4-character codes (FourCC) like INAM(Title), IART(Artist) or 
    ICMT(Comments).

    These codes are defined in RiffTagKey and are part of the standard RIFF specification. Each tag in the INFO chunk 
    follows the format: FourCC (4 chars) + data length (4 bytes) + data (UTF-8 text)

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
    rather than non-standard alternatives like ID3v2 tags.
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
        metadata_keys_direct_map_write = {
            AppMetadataKey.TITLE: self.RiffTagKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES: self.RiffTagKey.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.RiffTagKey.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: self.RiffTagKey.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: self.RiffTagKey.GENRE_NAME,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            # AppMetadataKey.TRACK_NUMBER: self.RiffTagKey.TRACK_NUMBER,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_255_NON_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_raw_metadata(self) -> FileType:
        self.audio_file.seek(0)
        return WAVE(io.BytesIO(self.audio_file.read()))

    def _convert_raw_metadata_to_dict(self) -> RawMetadataDict:
        """
        Convert RIFF INFO chunk metadata to dictionary.
        Only extracts tags from the INFO chunk.
        """
        file_raw_metadata_wav: WAVE = self.file_raw_metadata  # type: ignore
        if not file_raw_metadata_wav.tags:
            return {}

        # Extract only INFO chunk tags
        info_chunk = file_raw_metadata_wav.tags.get('INFO')
        if not info_chunk:
            return {}

        # Convert INFO chunk tags to RawMetadataDict
        return {self.RiffTagKey(key): [value] for key, value in info_chunk.items()}

    def _get_undirectly_mapped_metadata_value_other_than_rating(self, key: AppMetadataKey) -> AppMetadataValue:
        if key == AppMetadataKey.GENRE_NAME:
            genre_name = self.get_genre_name()
            return [genre_name] if genre_name else None
        else:
            raise UnsupportedMetadataError(f'Metadata key not handled: {key}')

    def get_genre_name(self) -> str | None:
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

    def get_track_number(self) -> int | None:
        part = self.file_raw_metadata.get(self.RiffTagKey.TRACK_NUMBER, None)
        if part:
            try:
                return int(part)
            except ValueError:
                return None
        return None

    def _update_formatted_value_in_raw_metadata(self, raw_metadata_key: RawMetadataKey, value: AppMetadataValue):
        file_raw_metadata_wav: WAVE = self.file_raw_metadata  # type: ignore

        # Ensure we have tags
        if not file_raw_metadata_wav.tags:
            file_raw_metadata_wav.add_tags()

        if file_raw_metadata_wav.tags is None:
            return

        # Ensure we have an INFO chunk
        if 'INFO' not in file_raw_metadata_wav.tags:
            file_raw_metadata_wav.tags['INFO'] = {}

        # Handle the value using FourCC code
        fourcc = raw_metadata_key  # Get the 4-character code
        if value is None and fourcc in file_raw_metadata_wav.tags['INFO']:
            del file_raw_metadata_wav.tags['INFO'][fourcc]
        elif value is not None:
            file_raw_metadata_wav.tags['INFO'][fourcc] = str(value)
