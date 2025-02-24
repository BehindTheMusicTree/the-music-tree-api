from typing import Optional
from mutagen.id3 import ID3
from mutagen.id3._frames import POPM, TALB, TCON, TIT2, TLAN, TPE1, TPE2, TDRC, TRCK, TBPM
from mutagen.id3._util import ID3NoHeaderError

from bodzify_api import settings
from ...audio_file import AudioFile
from ...AppMetadataKeys import AppMetadataKeys
from .Id3Manager import Id3Manager


class Id3v2Manager(Id3Manager):
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

    class Id3TextFrames:
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

    def __init__(self, audio_file: AudioFile):
        """Initialize ID3v2 manager and convert existing tags to v2.3 format.

        Args:
            audio_file: The audio file to manage metadata for
        """
        super().__init__(audio_file)

        try:
            tags = ID3(self.audio_file.file_path)
            tags.update_to_v23()  # Convert to ID3v2.3
            tags.save()  # Save the converted tags
        except ID3NoHeaderError:
            # Create new ID3v2.3 tag if none exists
            tags = ID3()
            tags.save(self.audio_file.file_path, v2_version=3)  # Explicitly save as ID3v2.3

    def get_raw_metadata(self) -> dict:
        try:
            tags = ID3(self.audio_file.file_path)
            # Force v2.3 update to ensure compatibility
            tags.update_to_v23()
            return tags  # type: ignore
        except ID3NoHeaderError:
            # Create new ID3 tag if none exists
            tags = ID3()
            tags.save(self.audio_file.file_path)
            return tags  # type: ignore

    def get_title(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(self.Id3TextFrames.TITLE)

    def get_artists_names(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(self.Id3TextFrames.ARTIST_NAME)

    def get_album_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(self.Id3TextFrames.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        album_artists_name_str_raw = (self._get_first_value_str_if_exists_in_file_metadata_or_none(
            self.Id3TextFrames.ALBUM_ARTISTS_NAMES))
        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> Optional[str]:
        if self.Id3TextFrames.GENRE_NAME in self.file_raw_metadata:
            return self.file_raw_metadata[self.Id3TextFrames.GENRE_NAME][0]
        else:
            return ""

    def get_eventually_normalized_rating_value(self, normalized_rating_max_value: int = 255):
        file_rating_value = None
        file_rating_email = None
        for key in self.file_raw_metadata:
            if self.Id3TextFrames.RATING in key:
                file_rating_tag = self.file_raw_metadata[key]
                file_rating_email = file_rating_tag.email
                file_rating_value = file_rating_tag.rating
                break
        if file_rating_value is None:
            return None
        else:
            return self._get_eventually_normalized_rating_from_file_rating(
                file_rating=file_rating_value,
                is_rating_from_traktor=(file_rating_email == self.TRAKTOR_RATING_TAG_MAIL),
                normalized_rating_max_value=normalized_rating_max_value)

    def get_language(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.Id3TextFrames.LANGUAGE)

    def get_release_date(self) -> Optional[str]:
        """Get release date from ID3 tags.

        Tries TDRC (ID3v2.4) first, then falls back to TYER (ID3v2.3) if needed.
        """
        # Try ID3v2.4 TDRC frame first
        date = self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.Id3TextFrames.RECORDING_TIME)
        if date:
            return date

        # Fall back to ID3v2.3 TYER frame
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.Id3TextFrames.YEAR)

    def get_track_number(self) -> Optional[int]:
        """Get track number from TRCK frame.

        The TRCK frame can contain either just a track number or 'track/total'
        format. This method extracts just the track number.
        """
        track = self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.Id3TextFrames.TRACK_NUMBER)
        if track:
            # Handle 'track/total' format by taking just the track number
            track = track.split('/')[0]
            try:
                return int(track)
            except ValueError:
                return None
        return None

    def get_bpm(self) -> Optional[float]:
        """Get BPM (Beats Per Minute) from TBPM frame.

        Returns:
            Optional[float]: BPM value if available, None otherwise
        """
        bpm = self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.Id3TextFrames.BPM)
        if bpm:
            try:
                return float(bpm)
            except ValueError:
                return None
        return None

    def update_specific_file_metadata_without_saving(
            self,
            normalized_metadata_value,
            app_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        if app_metadata_key == AppMetadataKeys.TITLE:
            id3_key = self.Id3TextFrames.TITLE
            text_frame_class = TIT2
        elif app_metadata_key == AppMetadataKeys.ARTISTS_NAMES_STR:
            id3_key = self.Id3TextFrames.ARTIST_NAME
            text_frame_class = TPE1
        elif app_metadata_key == AppMetadataKeys.ALBUM_NAME:
            id3_key = self.Id3TextFrames.ALBUM_NAME
            text_frame_class = TALB
        elif app_metadata_key == AppMetadataKeys.ALBUM_ARTISTS_NAMES_STR:
            id3_key = self.Id3TextFrames.ALBUM_ARTISTS_NAMES
            text_frame_class = TPE2
        elif app_metadata_key == AppMetadataKeys.GENRE_NAME:
            id3_key = self.Id3TextFrames.GENRE_NAME
            text_frame_class = TCON
        elif app_metadata_key == AppMetadataKeys.RATING:
            normalized_rating = normalized_metadata_value
            self.file_raw_metadata.delall(self.Id3TextFrames.RATING)  # type: ignore
            if normalized_rating:
                if normalized_rating_max_value is None:
                    normalized_rating_max_value = 255
                id3_rating = self._get_file_rating_from_normalized_rating(
                    normalized_rating=normalized_rating,
                    normalized_rating_max_value=normalized_rating_max_value,
                    rating_file_profile=self.RatingFileProfile.BASE_255)
                self.file_raw_metadata.add(POPM(email=self.ID3_RATING_APP_EMAIL, rating=id3_rating))  # type: ignore
            return
        elif app_metadata_key == AppMetadataKeys.LANGUAGE:
            id3_key = self.Id3TextFrames.LANGUAGE
            text_frame_class = TLAN
        elif app_metadata_key == AppMetadataKeys.RELEASE_DATE:
            id3_key = self.Id3TextFrames.RECORDING_TIME
            text_frame_class = TDRC
        elif app_metadata_key == AppMetadataKeys.TRACK_NUMBER:
            id3_key = self.Id3TextFrames.TRACK_NUMBER
            text_frame_class = TRCK
        elif app_metadata_key == AppMetadataKeys.BPM:
            id3_key = self.Id3TextFrames.BPM
            text_frame_class = TBPM
        else:
            raise KeyError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        self.file_raw_metadata.delall(id3_key)  # type: ignore
        self.file_raw_metadata.add(text_frame_class(encoding=3, text=normalized_metadata_value))  # type: ignore

    def _calculate_md5(self, audio_data):
        import hashlib
        md5_hash = hashlib.md5()
        md5_hash.update(audio_data)
        return md5_hash.hexdigest()

    def _get_stored_md5(self):
        if 'TXXX:MD5' in self.file_raw_metadata:
            return self.file_raw_metadata['TXXX:MD5'].text[0]
        else:
            return None

    def is_md5_valid(self, audio_data=None):
        if audio_data is None:
            self.audio_file.seek(0)
            audio_data = self.audio_file.read()

        # Calculate the MD5 checksum of the audio data
        calculated_md5 = self._calculate_md5(audio_data)

        # Retrieve the stored MD5 checksum from the ID3 metadata
        stored_md5 = self._get_stored_md5()

        # Compare the calculated and stored MD5 checksums
        return calculated_md5 == stored_md5

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
