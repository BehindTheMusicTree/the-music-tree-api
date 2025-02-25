"""Audio metadata handling module.

Metadata Support by Format:
+-----------------+--------------+--------------+--------------+-------------+-----------------+
| Field           |    ID3v1     |    ID3v2     |    Vorbis    |    RIFF     |   App Support   |
+-----------------+--------------+--------------+--------------+-------------+-----------------+
| Text Encoding   |    ASCII     | UTF-8/16/ISO |    UTF-8     | ASCII/UTF-8 |        -        |
+-----------------+--------------+--------------+--------------+-------------+-----------------+
| Operations      |      R       |      R/W     |     R/W      |    R/W      |        ✓        |
| supported       |(W using v2.4)|(W using v2.4)|              |             |                 |
+-----------------+--------------+--------------+--------------+-------------+-----------------+
| Technical Info  |              |              |              |             |                 |
| - Duration      |      ✓       |      ✓       |      ✓       |      ✓      |                 |
| - Bitrate       |      ✓       |      ✓       |      ✓       |      ✓      |        ✓        |
| - Sample Rate   |      ✓       |      ✓       |      ✓       |      ✓      |                 |
| - Channels      |      ✓       |      ✓       |      ✓       |      ✓      |                 |
| - File Size     |      ✓       |      ✓       |      ✓       |      ✓      |        ✓        |
| - Format Info   |      ✓       |      ✓       |      ✓       |      ✓      |                 |
| - MD5 Checksum  |              |              |      ✓       |             |    ✓ (Vorbis)   |
+-----------------+--------------+--------------+--------------+-------------+-----------------+
| Title           |    ✓ (30)    |      ✓       |      ✓       |      ✓      |        ✓        |
| Artist          |    ✓ (30)    |      ✓       |      ✓       |      ✓      |        ✓        |
| Album           |    ✓ (30)    |      ✓       |      ✓       |      ✓      |        ✓        |
| Album Artist    |              |      ✓       |      ✓       |             | ✓ (ID3v2/Vorbis)|
| Genre           |    ✓ (1)*    |      ✓       |      ✓       |     ✓*      |        ✓        |
| Release Date    |    ✓ (4)     |      ✓       |      ✓       |      ✓      |        ✓        |
| Track Number    |    ✓ (1)     |      ✓       |      ✓       |      ✓      |        ✓        |
| Disc Number     |              |      ✓       |      ✓       |             |                 |
| Rating          |              |      ✓       |      ✓       |             | ✓ (ID3v2/Vorbis)|
| BPM             |              |      ✓       |      ✓       |             | ✓ (ID3v2/Vorbis)|
| Language        |              |      ✓       |      ✓       |             | ✓ (ID3v2/Vorbis)|
| Composer        |              |      ✓       |      ✓       |      ✓      |                 |
| Publisher       |              |      ✓       |      ✓       |             |                 |
| Copyright       |              |      ✓       |      ✓       |      ✓      |                 |
| Lyrics          |              |      ✓       |      ✓       |             |                 |
| Comment         |    ✓ (28)    |      ✓       |      ✓       |      ✓      |                 |
| Encoder         |              |      ✓       |      ✓       |      ✓      |                 |
| URL             |              |      ✓       |      ✓       |             |                 |
| ISRC            |              |      ✓       |      ✓       |             |                 |
| Mood            |              |      ✓       |      ✓       |             |                 |
| Key             |              |      ✓       |      ✓       |             |                 |
| Original Date   |              |      ✓       |      ✓       |             |                 |
| Remixer         |              |      ✓       |      ✓       |             |                 |
| Conductor       |              |      ✓       |      ✓       |      ✓      |                 |
| Cover Art       |              |      ✓       |      ✓       |             |                 |
| Compilation     |              |      ✓       |      ✓       |             |                 |
| Media Type      |              |      ✓       |      ✓       |      ✓      |                 |
| File Owner      |              |      ✓       |      ✓       |             |                 |
| Recording Date  |              |      ✓       |      ✓       |             |                 |
| File Size       |              |      ✓       |              |             |                 |
| Encoder Settings|              |      ✓       |      ✓       |             |                 |
| ReplayGain      |              |      ✓       |      ✓       |             |                 |
| MusicBrainz ID  |              |      ✓       |      ✓       |             |                 |
| Arranger        |              |      ✓       |      ✓       |             |                 |
| Version         |              |      ✓       |      ✓       |             |                 |
| Performance     |              |      ✓       |      ✓       |             |                 |
| Archival Location|             |              |              |      ✓      |                 |
| Keywords        |              |              |              |      ✓      |                 |
| Subject         |              |              |              |      ✓      |                 |
| Original Artist |              |      ✓       |      ✓       |             |                 |
| Set Subtitle    |              |      ✓       |      ✓       |             |                 |
| Initial Key     |              |      ✓       |      ✓       |             |                 |
| Involved People |              |      ✓       |      ✓       |             |                 |
| Musicians       |              |      ✓       |      ✓       |             |                 |
| Part of Set     |              |      ✓       |      ✓       |             |                 |
+-----------------+--------------+--------------+--------------+-------------+-----------------+
Legend:
- ✓: Supported
- (30): Fixed 30-byte field
- *: Uses standard genre codes (0-147)
"""

from typing import Optional, Dict

from mutagen._file import FileType

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils.audio_metadata.utils.types import AppMetadataDict, RawMetadataDict, AppMetadataValue


from .exceptions import FileByteMismatchError
from .utils.AppMetadataKey import AppMetadataKey
from .utils.AudioFile import AudioFile
from .utils.TagFormat import TagFormat
from .manager.MetadataManager import MetadataManager
from .manager.rating_supporting.RiffManager import RiffManager
from .manager.id3v1.Id3v1Manager import Id3v1Manager
from .manager.rating_supporting.Id3v2Manager import Id3v2Manager
from .manager.rating_supporting.VorbisManager import VorbisManager


FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."

TAG_FORMAT_MANAGER_CLASS_MAP = {
    TagFormat.ID3V1: Id3v1Manager,
    TagFormat.ID3V2: Id3v2Manager,
    TagFormat.VORBIS: VorbisManager,
    TagFormat.RIFF: RiffManager
}


def _get_metadata_manager(
        file, tag_format: Optional[TagFormat] = None, normalized_rating_max_value: int | None = None) -> MetadataManager:
    audio_file = AudioFile(file)

    audio_file_prioritized_tag_formats = TagFormat.get_priorities().get(audio_file.file_extension)
    if not audio_file_prioritized_tag_formats:
        raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    if not tag_format:
        tag_format = audio_file_prioritized_tag_formats[0]
    else:
        if tag_format not in audio_file_prioritized_tag_formats:
            raise ImproperlyConfigured(
                f"Tag format {tag_format} not supported for file extension {audio_file.file_extension}")

    manager_class = TAG_FORMAT_MANAGER_CLASS_MAP[tag_format]
    return manager_class(audio_file=audio_file, normalized_rating_max_value=normalized_rating_max_value)


def _get_metadata_managers(
    file, tag_formats: Optional[list[TagFormat]] = None, normalized_rating_max_value: int | None = None
) -> Dict[TagFormat, MetadataManager]:
    audio_file = AudioFile(file)
    managers = {}

    if not tag_formats:
        tag_formats = TagFormat.get_priorities().get(audio_file.file_extension)
        if not tag_formats:
            raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    for tag_format in tag_formats:
        managers[tag_format] = _get_metadata_manager(
            file=file, tag_format=tag_format, normalized_rating_max_value=normalized_rating_max_value)
    return managers


def extract_raw_metadata_dict(file, tag_format: Optional[TagFormat] = None) -> FileType:
    return _get_metadata_manager(file, tag_format=tag_format).file_raw_metadata


def get_merged_normalized_metadata(file, normalized_rating_max_value: int | None = None) -> AppMetadataDict:
    try:
        audio_file = AudioFile(file)
    except Exception as error:
        error_str = str(error)
        if "file said" in error_str and "bytes, read" in error_str:
            raise FileByteMismatchError(error_str.capitalize())
        raise

    managers = _get_metadata_managers(file, normalized_rating_max_value=normalized_rating_max_value)
    metadata = {}

    # Get normalized metadata from each manager
    for tag_format, manager in managers.items():
        metadata[tag_format] = manager.get_app_metadata_dict()

    priorities = TagFormat.get_priorities().get(audio_file.file_extension, [])
    if not priorities:
        # Never reached because already checked in _get_metadata_managers
        raise ImproperlyConfigured(f"No priority order defined for {audio_file.file_extension}")

    result: AppMetadataDict = {}
    for field in AppMetadataKey:
        for tag_format in priorities:
            value = metadata[tag_format].get(field)
            if value is not None:
                result[field] = value
                break

    return result


def get_specific_metadata(file, app_metadata_key: AppMetadataKey) -> AppMetadataValue:
    value = _get_metadata_manager(file).get_app_specific_metadata(app_metadata_key=app_metadata_key)
    if value is not None and isinstance(value, AppMetadataValue):
        return value
    return ""  # Return empty string as fallback


def update_metadata(file, app_metadata_dict: AppMetadataDict):
    _get_metadata_manager(file,).update_bulk(app_metadata_dict=app_metadata_dict)


def delete_metadata(file, tag_format: Optional[TagFormat] = None) -> bool:
    return _get_metadata_manager(file, tag_format=tag_format).delete_metadata()


def get_bitrate(file) -> int:
    return AudioFile(file).get_bitrate()


def get_duration_in_sec(file) -> float:
    return AudioFile(file).get_duration()


def is_flac_md5_valid(file, check_id3v2: bool = False):
    audio_file = AudioFile(file)

    if audio_file.file_extension == ".flac":
        if check_id3v2:
            id3v2_tags = Id3v2Manager(audio_file).file_raw_metadata
            if id3v2_tags:
                return False
        return audio_file.is_flac_file_md5_valid()
    else:
        raise ImproperlyConfigured('The file must be a FLAC file to check the MD5.')


def replace_flac_with_corrected_md5(file):
    return AudioFile(file).replace_flac_with_corrected_md5()
