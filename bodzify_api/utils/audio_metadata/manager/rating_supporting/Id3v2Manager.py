
from typing import Dict, Type
from mutagen.id3 import ID3
from mutagen.id3._frames import POPM, TALB, TCON, TIT2, TLAN, TPE1, TPE2, TDRC, TRCK, TBPM, TYER
from mutagen.id3._util import ID3NoHeaderError

from bodzify_api import settings

from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import RawMetadataDict, RawMetadataKey
from ...utils.AudioFile import AudioFile
from ...utils.AppMetadataKey import AppMetadataKey
from .RatingSupportingMetadataManager import RatingSupportingMetadataManager


class Id3v2Manager(RatingSupportingMetadataManager):
    """ID3v2 metadata manager for audio files.

    ID3v2 Version Compatibility Table:
    +---------------+----------+----------+----------+
    | Player/Device | ID3v2.2  | ID3v2.3  | ID3v2.4  |
    +---------------+----------+----------+----------+
    | Windows Media Player                           |
    |  - WMP 9-12   |    ✓     |    ✓     |    ~     |
    |  - WMP 7-8    |    ✓     |    ✓     |          |
    +---------------+----------+----------+----------+
    | iTunes                                         |
    |  - 12.x+      |    ✓     |    ✓     |    ✓     |
    |  - 7.x-11.x   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Winamp                                         |
    |  - 5.x+       |    ✓     |    ✓     |    ✓     |
    |  - 2.x-4.x    |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | MusicBee                                       |
    |  - 3.x+       |    ✓     |    ✓     |    ✓     |
    |  - 2.x        |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | VLC                                            |
    |  - 2.x+       |    ✓     |    ✓     |    ✓     |
    |  - 1.x        |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Smartphones                                    |
    |  - iOS 7+     |    ✓     |    ✓     |    ✓     |
    |  - Android 4+ |    ✓     |    ✓     |    ✓     |
    |  - Windows    |    ✓     |    ✓     |    ✓     |
    |  - Blackberry |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Network Players                                |
    |  - Sonos      |    ✓     |    ✓     |    ✓     |
    |  - Roku       |    ✓     |    ✓     |    ~     |
    |  - Chromecast |    ✓     |    ✓     |    ✓     |
    |  - Apple TV   |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+
    |iPods/MP3 Players                               |
    |  - iPod 5G+   |    ✓     |    ✓     |    ✓     |
    |  - iPod 1-4G  |    ✓     |    ✓     |    ~     |
    |  - Zune       |    ✓     |    ✓     |    ~     |
    |  - Sony       |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Car Systems                                    |
    |  - Post-2010  |    ✓     |    ✓     |    ~     |
    |  - Pre-2010   |    ✓     |    ~     |          |
    +---------------+----------+----------+----------+
    | Home Audio Systems                             |
    |  - Post-2000  |    ✓     |    ✓     |    ~     |
    |  - Pre-2000   |    ✓     |    ~     |          |
    +---------------+----------+----------+----------+
    | DJ Software                                    |
    |  - Traktor    |    ✓     |    ✓     |    ✓     |
    |  - Serato     |    ✓     |    ✓     |    ~     |
    |  - VirtualDJ  |    ✓     |    ✓     |    ~     |
    |  - Rekordbox  |    ✓     |    ✓     |    ~     |
    |  - Mixxx      |    ✓     |    ✓     |    ~     |
    |  - Cross DJ   |    ✓     |    ✓     |    ~     |
    |  - djay Pro   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Web Browsers                                   |
    |  - Chrome     |    ✓     |    ✓     |    ✓     |
    |  - Firefox    |    ✓     |    ✓     |    ✓     |
    |  - Safari     |    ✓     |    ✓     |    ✓     |
    |  - Edge       |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+
    | Gaming Consoles                                |
    |  - PS4/PS5    |    ✓     |    ✓     |    ✓     |
    |  - Xbox Series|    ✓     |    ✓     |    ✓     |
    |  - PS3        |    ✓     |    ✓     |    ~     |
    |  - Xbox 360   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Smart TVs                                      |
    |  - Samsung    |    ✓     |    ✓     |    ~     |
    |  - LG         |    ✓     |    ✓     |    ~     |
    |  - Sony       |    ✓     |    ✓     |    ~     |
    |  - Android TV |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+

    Legend:
    ✓ = Full support
    ~ = Partial support/May have issues
      = No support

    Notes:
    - ID3v2.4 introduced UTF-8 encoding and unsync changes
    - Older players may have issues with ID3v2.4's changes
    - For maximum compatibility, ID3v2.3 is recommended

    - ID3:
        - Writing Policy:
            * The app always writes ID3v2 tags in v2.4 format
            * When updating an existing file:
                - v2.4 tags are updated in place
                - v2.3 or v2.2 tags are upgraded to v2.4
                - Frame IDs are automatically converted
                - All text is encoded in UTF-8
            * Reading supports all versions (v2.2, v2.3, v2.4)
            * Only one ID3v2 version can exist in a file at a time
            * Native format for MP3 files

        - ID3v1:
            * Fixed 128-byte format at end of file
            * ASCII only, no Unicode
            * Limited to 30 chars for text fields
            * Single byte for track number (v1.1 only)
            * Genre limited to predefined codes (0-147)
            * Legacy format, read-only support

        - ID3v2:
            * v2.2:
                - Introduced in 1998
                - Three-character frame IDs (TT2, TP1, etc.)
                - ISO-8859-1 or UCS-2 text encoding
                - All standard fields supported
                - Simpler header structure than v2.3/v2.4
                - Basic support for embedded images
                - Less common but equally functional

            * v2.3:
                - Introduced in 1999
                - TYER+TDAT frames for date (year and date separately)
                - UTF-16/UTF-16BE text encoding
                - Basic unsynchronization
                - All metadata fields supported
                - Better support for embedded images and other binary data
                - Most widely used version

            * v2.4:
                - Introduced in 2000
                - TDRC frame for full timestamps (YYYY-MM-DD)
                - UTF-8 text encoding
                - Extended header features
                - Unsynchronization per frame
                - All metadata fields supported
                - New frames for more detailed metadata (e.g., TDRC for recording time, TDRL for release time)
                - Preferred version for new tags

    For the most compatibility, ID3v2.3 will be used as the version for writing metadata.
    Thus when reading/updating an existing file, the ID3 tags will be updated to v2.3 format.
    """

    ID3_RATING_APP_EMAIL = settings.APP_NAME

    class Id3TextFrame(RawMetadataKey):
        TITLE = 'TIT2'
        ARTIST_NAME = 'TPE1'
        ALBUM_NAME = 'TALB'
        ALBUM_ARTISTS_NAMES = 'TPE2'
        GENRE_NAME = 'TCON'
        RATING = 'POPM'
        LANGUAGE = 'TLAN'
        RECORDING_TIME = 'TDRC'  # ID3v2.4 recording time
        YEAR = 'TYER'  # ID3v2.3 year
        TRACK_NUMBER = 'TRCK'
        BPM = 'TBPM'

    ID3_TEXT_FRAME_CLASS_MAP = {
        Id3TextFrame.TITLE: TIT2,
        Id3TextFrame.ARTIST_NAME: TPE1,
        Id3TextFrame.ALBUM_NAME: TALB,
        Id3TextFrame.ALBUM_ARTISTS_NAMES: TPE2,
        Id3TextFrame.GENRE_NAME: TCON,
        Id3TextFrame.LANGUAGE: TLAN,
        Id3TextFrame.RECORDING_TIME: TDRC,
        Id3TextFrame.YEAR: TYER,
        Id3TextFrame.TRACK_NUMBER: TRCK,
        Id3TextFrame.BPM: TBPM,
    }

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: int | None = None):
        metadata_keys_direct_map_read = {
            AppMetadataKey.TITLE: self.Id3TextFrame.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.Id3TextFrame.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.Id3TextFrame.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: self.Id3TextFrame.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: self.Id3TextFrame.GENRE_NAME,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.Id3TextFrame.LANGUAGE,
        }
        metadata_keys_direct_map_write: Dict = {
            AppMetadataKey.TITLE: self.Id3TextFrame.TITLE,
            AppMetadataKey.ARTISTS_NAMES_STR: self.Id3TextFrame.ARTIST_NAME,
            AppMetadataKey.ALBUM_NAME: self.Id3TextFrame.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES_STR: self.Id3TextFrame.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: self.Id3TextFrame.GENRE_NAME,
            AppMetadataKey.RATING: self.Id3TextFrame.RATING,
            AppMetadataKey.LANGUAGE: self.Id3TextFrame.LANGUAGE,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_255_NON_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_raw_metadata(self) -> RawMetadataDict:
        try:
            tags = ID3(self.audio_file.get_file_path_or_object())
            # Force v2.3 update to ensure compatibility
            tags.update_to_v23()
            return tags
        except ID3NoHeaderError:
            tags = ID3()
            tags.save(self.audio_file.get_file_path_or_object(), v2_version=3)
            return {}

    def _update_value_in_raw_metadata(self, raw_metadata_key: RawMetadataKey, value: str | int | float | None):
        id3_key: Type[self.Id3TextFrame] = raw_metadata_key
        self.file_raw_metadata.delall(id3_key)  # type: ignore
        text_frame_class = self.ID3_TEXT_FRAME_CLASS_MAP[raw_metadata_key]
        self.file_raw_metadata.add(text_frame_class(encoding=3, text=app_metadata_value))  # type: ignore
        return super()._update_value_in_raw_metadata(raw_metadata_key, value)

    def get_title(self) -> str | None:
        return self._get_first_value_in_raw_metadata_dict_or_none(self.Id3TextFrame.TITLE, str)

    def get_artists_names(self) -> str | None:
        return self._get_first_value_str_if_exists_in_str_dict_or_none(self.Id3TextFrame.ARTIST_NAME)

    def get_album_name(self) -> str | None:
        return self._get_first_value_str_if_exists_in_str_dict_or_none(self.Id3TextFrame.ALBUM_NAME)

    def get_album_artists_name_str(self) -> str | None:
        album_artists_name_str_raw = (self._get_first_value_str_if_exists_in_str_dict_or_none(
            self.Id3TextFrame.ALBUM_ARTISTS_NAMES))
        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> str | None:
        if self.Id3TextFrame.GENRE_NAME in self.file_raw_metadata:
            return self.file_raw_metadata[self.Id3TextFrame.GENRE_NAME][0]
        else:
            return ""

    def _get_eventually_normalized_rating_from_file(self) -> int | None:
     file_rating_value = None
      file_rating_email = None
       for key in self.file_raw_metadata:
            if self.Id3TextFrame.RATING in key:
                file_rating_tag = self.file_raw_metadata[key]
                file_rating_email = file_rating_tag.email
                file_rating_value = file_rating_tag.rating
                break
        if file_rating_value is None:
            return None
        else:
            return self._convert_file_rating_to_eventually_normalized_rating(
                file_rating=file_rating_value,
                is_rating_from_traktor=(file_rating_email == self.TRAKTOR_RATING_TAG_MAIL))

    def get_track_number(self) -> int | None:
        """Get track number from TRCK frame.

        The TRCK frame can contain either just a track number or 'track/total'
        format. This method extracts just the track number.
        """
        track = self._get_first_value_str_if_exists_in_str_dict_or_none(key=self.Id3TextFrame.TRACK_NUMBER)
        if track:
            # Handle 'track/total' format by taking just the track number
            track = track.split('/')[0]
            try:
                return int(track)
            except ValueError:
                return None
        return None

    def _update_undirectly_mapped_metadata(
            self, app_metadata_value, app_metadata_key: str, normalized_rating_max_value: int | None = None):
        if app_metadata_key == AppMetadataKey.TITLE:
            id3_key = self.Id3TextFrame.TITLE
            text_frame_class = TIT2
        elif app_metadata_key == AppMetadataKey.ARTISTS_NAMES_STR:
            id3_key = self.Id3TextFrame.ARTIST_NAME
            text_frame_class = TPE1
        elif app_metadata_key == AppMetadataKey.ALBUM_NAME:
            id3_key = self.Id3TextFrame.ALBUM_NAME
            text_frame_class = TALB
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            id3_key = self.Id3TextFrame.ALBUM_ARTISTS_NAMES
            text_frame_class = TPE2
        elif app_metadata_key == AppMetadataKey.GENRE_NAME:
            id3_key = self.Id3TextFrame.GENRE_NAME
            text_frame_class = TCON
        elif app_metadata_key == AppMetadataKey.RATING:
            normalized_rating = app_metadata_value
            self.file_raw_metadata.delall(self.Id3TextFrame.RATING)  # type: ignore
            if normalized_rating:
                if normalized_rating_max_value is None:
                    normalized_rating_max_value = 255
                id3_rating = self._convert_normalized_rating_to_file_rating(
                    normalized_rating=normalized_rating,
                    normalized_rating_max_value=normalized_rating_max_value,
                    rating_writing_profile=RatingWriteProfile.BASE_255_PROPORTIONAL)
                self.file_raw_metadata.add(POPM(email=self.ID3_RATING_APP_EMAIL, rating=id3_rating))  # type: ignore
            return
        elif app_metadata_key == AppMetadataKey.LANGUAGE:
            id3_key = self.Id3TextFrame.LANGUAGE
            text_frame_class = TLAN
        elif app_metadata_key == AppMetadataKey.RELEASE_DATE:
            id3_key = self.Id3TextFrame.RECORDING_TIME
            text_frame_class = TDRC
        elif app_metadata_key == AppMetadataKey.TRACK_NUMBER:
            id3_key = self.Id3TextFrame.TRACK_NUMBER
            text_frame_class = TRCK
        elif app_metadata_key == AppMetadataKey.BPM:
            id3_key = self.Id3TextFrame.BPM
            text_frame_class = TBPM
        else:
            raise KeyError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        self.file_raw_metadata.delall(id3_key)  # type: ignore
        self.file_raw_metadata.add(text_frame_class(encoding=3, text=app_metadata_value))  # type: ignore

    def delete_metadata(self) -> bool:
        """Delete all ID3v2 metadata from the audio file.

        This removes all ID3v2 frames from the file while preserving the audio data.
        Uses ID3.delete() which is more reliable than deleting individual frames,
        especially for non-MP3 files like FLAC that might have ID3v2 tags.

        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Create a new ID3 instance and use delete() to remove all ID3v2 tags
            id3 = ID3(self.audio_file.file_path)
            id3.delete()
            return True
        except ID3NoHeaderError:
            # No ID3 tags present, consider this a success
            return True
        except Exception:
            return False
