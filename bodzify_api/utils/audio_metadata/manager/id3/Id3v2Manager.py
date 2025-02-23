from typing import Optional
from mutagen.id3._frames import POPM, TALB, TCON, TIT2, TLAN, TPE1, TPE2, TDRC, TRCK, TBPM

from bodzify_api import settings

from .Id3Manager import Id3Manager
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys


class Id3v2Manager(Id3Manager):
    """
    Manages ID3v2 metadata for audio files.

    ID3v2 is a metadata format introduced in 1998, located at the beginning of audio files.
    It offers extensive metadata support with variable-size tags and Unicode encoding.
    See Id3Manager module docstring for comprehensive ID3 format support documentation.

    Key Features:
    - Variable size tags at file start
    - Unicode text support
    - Extensive metadata fields via frames:
        - Title (TIT2)
        - Artist (TPE1)
        - Album (TALB)
        - Year (TDRC/TYER)
        - Genre (TCON)
        - Track number (TRCK)
        - Album artist (TPE2)
        - Language (TLAN)
        - BPM (TBPM)
        - Rating (POPM)
        - And many more...
    """

    ID3_RATING_APP_EMAIL = settings.APP_NAME

    class Id3TextFrames:  # MP3 and Wave (.wav) files use ID3 tags
        TITLE = 'TIT2'
        ARTIST_NAME = 'TPE1'
        ALBUM_NAME = 'TALB'
        ALBUM_ARTISTS_NAMES = 'TPE2'
        GENRE_NAME = 'TCON'
        RATING = 'POPM'
        LANGUAGE = 'TLAN'
        RECORDING_TIME = 'TDRC'  # ID3v2.4 recording time
        YEAR = 'TYER'  # ID3v2.3 year
        TRACK_NUMBER = 'TRCK'  # Track number/Position in set
        BPM = 'TBPM'  # Beats Per Minute

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

    def get_position_in_album(self) -> Optional[int]:
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
            normalized_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        if normalized_metadata_key == NormalizedMetadataKeys.TITLE:
            id3_key = self.Id3TextFrames.TITLE
            text_frame_class = TIT2
        elif normalized_metadata_key == NormalizedMetadataKeys.ARTISTS_NAMES_STR:
            id3_key = self.Id3TextFrames.ARTIST_NAME
            text_frame_class = TPE1
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_NAME:
            id3_key = self.Id3TextFrames.ALBUM_NAME
            text_frame_class = TALB
        elif normalized_metadata_key == NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES_STR:
            id3_key = self.Id3TextFrames.ALBUM_ARTISTS_NAMES
            text_frame_class = TPE2
        elif normalized_metadata_key == NormalizedMetadataKeys.GENRE_NAME:
            id3_key = self.Id3TextFrames.GENRE_NAME
            text_frame_class = TCON
        elif normalized_metadata_key == NormalizedMetadataKeys.RATING:
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
        elif normalized_metadata_key == NormalizedMetadataKeys.LANGUAGE:
            id3_key = self.Id3TextFrames.LANGUAGE
            text_frame_class = TLAN
        elif normalized_metadata_key == NormalizedMetadataKeys.RELEASE_DATE:
            id3_key = self.Id3TextFrames.RECORDING_TIME
            text_frame_class = TDRC
        elif normalized_metadata_key == NormalizedMetadataKeys.POSITION_IN_ALBUM:
            id3_key = self.Id3TextFrames.TRACK_NUMBER
            text_frame_class = TRCK
        elif normalized_metadata_key == NormalizedMetadataKeys.BPM:
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