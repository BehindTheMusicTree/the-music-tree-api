import io
import subprocess
from typing import Optional

from mutagen.flac import FLAC
from mutagen.id3._util import ID3NoHeaderError
from mutagen.id3 import ID3

from bodzify_api.utils.audio_metadata.manager.MetadataManager import MetadataManager, AppMetadataKey
from bodzify_api.utils.audio_metadata.exceptions import InvalidChunkDecodeError


class VorbisManager(MetadataManager):
    """
    Manages Vorbis comments for audio files.

    Vorbis comments are used to store metadata in audio files, primarily in formats like Ogg Vorbis and FLAC.
    They are more flexible and extensible compared to ID3 tags, allowing for a wide range of metadata fields.

    Genre Support:
    Like ID3v2 but unlike ID3v1 and RIFF, Vorbis comments support:
    - Custom genre names as free text
    - Multiple genres (comma-separated)
    - No length limitations
    - Unicode support for international genres
    - No predefined genre list restrictions

    Vorbis comments are key-value pairs, where the key is a field name and the value is the corresponding metadata.
    Common fields include:
    - TITLE: The title of the track.
    - ARTIST: The artist or performer.
    - ALBUM: The name of the album.
    - TRACKNUMBER: The track number on the album.
    - GENRE: The genre name of the track.
    - DATE: The date of the recording.
    - COMMENT: Any additional comments.
    - ALBUMARTIST: The album artist.
    - COMPOSER: The composer of the track.
    - PERFORMER: The performer of the track.
    - COPYRIGHT: Copyright information.
    - LICENSE: Licensing information.
    - ORGANIZATION: The organization or label.
    - DESCRIPTION: A description of the track.
    - LOCATION: The location where the track was recorded.
    - CONTACT: Contact information.
    - ISRC: International Standard Recording Code.
    - ENCODEDBY: The person or software that encoded the track.
    - BPM: Beats per minute.
    - LANGUAGE: The language of the track.
    - RATING: The rating of the track.

    Compatible Extensions:
    - Ogg Vorbis: Fully supports Vorbis comments.
    - FLAC: Fully supports Vorbis comments.
    - Opus: Fully supports Vorbis comments.

    Note: This class assumes that the audio files being managed are primarily in formats that support Vorbis comments.
    """

    class VorbisTagKeys:
        TITLE = 'title'
        ARTIST_NAME = 'artist'
        ALBUM_NAME = 'album'
        ALBUM_ARTISTS_NAMES = 'albumartist'
        GENRE_NAME = 'genre'
        RATING = 'rating'
        RATING_TRAKTOR = 'rating wmp'
        LANGUAGE = 'language'

        DATE = 'date'
        TRACK_NUMBER = 'tracknumber'
        BPM = 'bpm'

    def is_md5_valid(self) -> bool:
        self.audio_file.seek(0)
        result = subprocess.run(
            ['flac', '-t', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=self.audio_file.read())

        output = result.stderr.decode()
        if 'ok' in output:
            return True
        if 'MD5 signature mismatch' in output:
            return False
        else:
            raise Exception("The Flac file md5 check failed")

    def get_raw_metadata(self) -> dict:
        self.audio_file.seek(0)
        try:
            flac_file = FLAC(io.BytesIO(self.audio_file.read()))
            return {
                'info': flac_file.info.__dict__,
                'tags': flac_file.tags,
                'pictures': [picture.__dict__ for picture in flac_file.pictures],
                'cuesheet': flac_file.cuesheet.__dict__ if flac_file.cuesheet else None,
                'seektable': flac_file.seektable.__dict__ if flac_file.seektable else None,
            }
        except Exception as error:
            error_str = str(error)
            if "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
                raise InvalidChunkDecodeError(error_str)
            raise

    def get_eventually_normalized_rating_value(self,
                                               normalized_rating_max_value: Optional[int] = None) -> Optional[int]:
        file_rating = self._get_first_value_int_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.RATING)
        is_rating_from_traktor = False
        if file_rating is None:
            file_rating = self._get_first_value_int_if_exists_in_file_metadata_or_none(
                key=self.VorbisTagKeys.RATING_TRAKTOR)
            if file_rating:
                is_rating_from_traktor = True

        if file_rating is None or file_rating == "":
            return None
        else:
            return self._get_eventually_normalized_rating_from_file_rating(
                file_rating=file_rating,
                is_rating_from_traktor=is_rating_from_traktor,
                normalized_rating_max_value=normalized_rating_max_value)

    def get_title(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.TITLE)

    def get_artists_names(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.ARTIST_NAME)

    def get_album_name(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.ALBUM_NAME)

    def get_album_artists_name_str(self) -> Optional[str]:
        album_artists_name_str_raw = self._get_first_value_str_if_exists_in_file_metadata_or_none(
            key=self.VorbisTagKeys.ALBUM_ARTISTS_NAMES)
        if album_artists_name_str_raw:
            return album_artists_name_str_raw.strip()
        return None

    def get_genre_name(self) -> Optional[str]:
        if self.VorbisTagKeys.GENRE_NAME in self.file_raw_metadata:
            return self.file_raw_metadata[self.VorbisTagKeys.GENRE_NAME][0]
        else:
            return ""

    def get_language(self) -> Optional[str]:
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.LANGUAGE)

    def get_release_date_str(self) -> Optional[str]:
        """Get release date from DATE tag."""
        return self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.DATE)

    def get_track_number(self) -> Optional[int]:
        """Get track number from TRACKNUMBER tag.

        Returns:
            Optional[int]: Track number if available, None otherwise
        """
        track = self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.TRACK_NUMBER)
        if track:
            try:
                return int(track)
            except ValueError:
                return None
        return None

    def get_bpm(self) -> Optional[float]:
        """Get BPM (Beats Per Minute) from BPM tag.

        Returns:
            Optional[float]: BPM value if available, None otherwise
        """
        bpm = self._get_first_value_str_if_exists_in_file_metadata_or_none(key=self.VorbisTagKeys.BPM)
        if bpm:
            try:
                return float(bpm)
            except ValueError:
                return None
        return None

    def update_specific_without_saving(
            self,
            normalized_metadata_value,
            app_metadata_key: str,
            normalized_rating_max_value: Optional[int] = None):
        if app_metadata_key == AppMetadataKey.TITLE:
            vorbis_tag_key = self.VorbisTagKeys.TITLE
        elif app_metadata_key == AppMetadataKey.ARTISTS_NAMES_STR:
            vorbis_tag_key = self.VorbisTagKeys.ARTIST_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_NAME:
            vorbis_tag_key = self.VorbisTagKeys.ALBUM_NAME
        elif app_metadata_key == AppMetadataKey.ALBUM_ARTISTS_NAMES_STR:
            vorbis_tag_key = self.VorbisTagKeys.ALBUM_ARTISTS_NAMES
        elif app_metadata_key == AppMetadataKey.GENRE_NAME:
            vorbis_tag_key = self.VorbisTagKeys.GENRE_NAME
        elif app_metadata_key == AppMetadataKey.RATING:
            app_rating = normalized_metadata_value
            vorbis_tag_key = self.VorbisTagKeys.RATING
            if app_rating:
                vorbis_rating = self._get_file_rating_from_normalized_rating(
                    normalized_rating=app_rating,
                    normalized_rating_max_value=normalized_rating_max_value,  # type: ignore
                    rating_file_profile=self.RatingFileProfile.BASE_100)
                normalized_metadata_value = str(vorbis_rating)
        elif app_metadata_key == AppMetadataKey.LANGUAGE:
            vorbis_tag_key = self.VorbisTagKeys.LANGUAGE
        elif app_metadata_key == AppMetadataKey.RELEASE_DATE:
            vorbis_tag_key = self.VorbisTagKeys.DATE
        elif app_metadata_key == AppMetadataKey.TRACK_NUMBER:
            vorbis_tag_key = self.VorbisTagKeys.TRACK_NUMBER
        elif app_metadata_key == AppMetadataKey.BPM:
            vorbis_tag_key = self.VorbisTagKeys.BPM
        else:
            raise KeyError(self.METADATA_UPDATE_KEY_NOT_HANDLED_MESSAGE)

        if normalized_metadata_value:
            if vorbis_tag_key not in self.file_raw_metadata:
                self.file_raw_metadata[vorbis_tag_key] = [1]
            self.file_raw_metadata[vorbis_tag_key] = normalized_metadata_value
        elif vorbis_tag_key in self.file_raw_metadata:
            del self.file_raw_metadata[vorbis_tag_key]

    def delete_metadata(self) -> bool:
        """Delete all metadata from the FLAC/Vorbis file.

        This removes:
        - All Vorbis comment tags
        - All pictures/album art
        - Cuesheet if present
        - Any ID3 tags that might be present

        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Read the file into memory
            self.audio_file.seek(0)
            flac_file = FLAC(io.BytesIO(self.audio_file.read()))

            # Clear all Vorbis comments
            flac_file.tags = None

            # Clear all pictures
            flac_file.clear_pictures()

            # Clear cuesheet
            flac_file.cuesheet = None

            # Save changes back to the file
            flac_file.save(self.audio_file.file_path)

            # Also remove any ID3 tags that might be present
            try:
                id3 = ID3(self.audio_file.file_path)
                id3.delete()
            except (ID3NoHeaderError, ImportError):
                pass  # No ID3 tags present or ID3 support not available

            return True
        except Exception:
            return False
