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

import tempfile
import os
import subprocess
from typing import Optional, Dict, cast, Union

from django.db.models.fields.files import FieldFile
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils.audio_metadata.types import AppMetadataDict, RawMetadataDict, TagValue


from .exceptions import FileByteMismatchError, FlacMd5CheckFailedError, InvalidChunkDecodeError
from .AppMetadataKey import AppMetadataKey
from .AudioFile import AudioFile
from .TagFormat import TagFormat
from .manager.MetadataManager import MetadataManager
from .manager.riff.RiffManager import RiffManager
from .manager.id3.Id3v1Manager import Id3v1Manager
from .manager.id3.Id3v2Manager import Id3v2Manager
from .manager.vorbis.VorbisManager import VorbisManager


FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."

TAG_FORMAT_MANAGER_MAP = {
    TagFormat.ID3V1: Id3v1Manager,
    TagFormat.ID3V2: Id3v2Manager,
    TagFormat.VORBIS: VorbisManager,
    TagFormat.RIFF: RiffManager
}


def _get_metadata_manager(file, tag_format: Optional[TagFormat] = None) -> MetadataManager:
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

    return TAG_FORMAT_MANAGER_MAP[tag_format](audio_file)


def _get_metadata_managers(file, tag_formats: Optional[list[TagFormat]] = None) -> dict[TagFormat, MetadataManager]:
    audio_file = AudioFile(file)
    managers = {}

    if not tag_formats:
        tag_formats = TagFormat.get_priorities().get(audio_file.file_extension)
        if not tag_formats:
            raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    for tag_format in tag_formats:
        managers[tag_format] = _get_metadata_manager(file, tag_format)
    return managers


def get_raw_metadata(file, tag_format: Optional[TagFormat] = None) -> RawMetadataDict:
    return _get_metadata_manager(file, tag_format=tag_format).file_raw_metadata


def get_merged_normalized_metadata(file, normalized_rating_max_value: Optional[int] = None) -> AppMetadataDict:
    audio_file = AudioFile(file)
    try:
        managers = _get_metadata_managers(file)
        metadata = {}

        for tag_format, manager in managers.items():
            metadata[tag_format] = manager.get_normalized_metadata(normalized_rating_max_value)

        priorities = TagFormat.get_priorities().get(audio_file.file_extension, [])
        if not priorities:
            # Never reached because already checked in _get_metadata_managers
            raise ImproperlyConfigured(f"No priority order defined for {audio_file.file_extension}")

        merged_metadata: AppMetadataDict = {}
        for field in AppMetadataKey:
            for tag_format in priorities:
                value = metadata[tag_format].get(field)
                if value is not None:
                    merged_metadata[field] = value
                    break
        return merged_metadata

    except Exception as error:
        error_str = str(error)
        if "file said" in error_str and "bytes, read" in error_str:
            raise FileByteMismatchError(error_str.capitalize())
        elif "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
            raise InvalidChunkDecodeError(error_str)
        raise


def get_specific_metadata(
        file, app_metadata_key: str, tag_format: Optional[TagFormat] = None) -> TagValue:
    manager = _get_metadata_manager(file, tag_format=tag_format)
    value = manager.get_specific_file_metadata(app_metadata_key=app_metadata_key)
    if value is not None and isinstance(value, (str, int)):
        return value
    return ""  # Return empty string as fallback


def get_bitrate(file) -> int:
    return AudioFile(file).get_bitrate()


def get_prioritized_metadata(
        file, normalized_rating_max_value: Optional[int] = None) -> Dict[str, TagValue]:
    """Get merged metadata prioritizing certain tag types based on file format.

    For FLAC files: Prioritizes Vorbis comments over ID3v2 tags
    For MP3 files: Uses ID3v2 tags
    For WAV files: Uses RIFF metadata

    Args:
        file: The audio file to analyze
        normalized_rating_max_value: Optional max value for normalizing ratings

    Returns:
        Dictionary with merged metadata using tag type priorities
    """
    audio_file = AudioFile(file)

    # Determine which tag types to check based on file extension
    tag_formats = TagFormat.get_priorities().get(audio_file.file_extension.lower())

    if not tag_formats:
        raise ImproperlyConfigured(f"File type {audio_file.file_extension} not supported")

    # Get metadata from all relevant tag types and merge with priority
    metadata = get_merged_normalized_metadata(
        file,
        normalized_rating_max_value=normalized_rating_max_value
    )

    # Convert AppMetadataKey to str in the return value
    merged_data = metadata['merged']
    return {str(key): value for key, value in merged_data.items()}


def update_metadata(file, normalized_metadata: dict, normalized_rating_max_value: int):
    """Update metadata using the highest priority manager for the file type.

    For FLAC files: Uses Vorbis comments (preferred over ID3v2)
    For MP3 files: Uses ID3v2 tags (preferred over ID3v1)
    For WAV files: Uses RIFF metadata

    Args:
        file: The audio file to update
        normalized_metadata: Dictionary of normalized metadata to write
        normalized_rating_max_value: Max value for normalizing ratings

    Raises:
        ImproperlyConfigured: If the file type is not supported
    """
    audio_file = AudioFile(file)
    priorities = TagFormat.get_priorities().get(audio_file.file_extension.lower())
    if not priorities:
        raise ImproperlyConfigured(f"File type {audio_file.file_extension} not supported")

    primary_tag_format = priorities[0]

    # Get the manager for just this tag type
    manager = _get_metadata_manager(file, tag_format=primary_tag_format)
    if not manager:
        raise ImproperlyConfigured(
            f"Could not get {primary_tag_format} manager for {audio_file.file_extension}")

    # Use the primary manager for updates
    manager.update_file_metadata(
        normalized_metadata=normalized_metadata,
        normalized_rating_max_value=normalized_rating_max_value)


def delete_metadata(file, tag_format: Optional[TagFormat] = None) -> dict[TagFormat, bool]:
    manager = _get_metadata_manager(file, tag_format=tag_format)
    results = {}
    if manager:
        results[tag_format if tag_format else TagFormat.ID3V2] = manager.delete_metadata()
        results[tag_format] = manager.delete_metadata()
    return results


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
    audio_file = AudioFile(file)

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name

    # Run FLAC and save to temporary file
    result = subprocess.run(
        ['flac', '-f', '--best', '-o', temp_path, '-'],
        input=audio_file.read(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stderr = result.stderr.decode()
    if 'wrote' not in stderr:
        raise FlacMd5CheckFailedError(
            "The Flac file md5 check failed and could not be corrected. The file is probably corrupted.")

    # Replace original file content with corrected content
    if isinstance(audio_file.file, (TemporaryUploadedFile, InMemoryUploadedFile)):
        audio_file.seek(0)
        with open(temp_path, 'rb') as f:
            audio_file.write(f.read())
    elif isinstance(audio_file.file, FieldFile):
        with audio_file.file.open('wb') as f, open(temp_path, 'rb') as temp_f:
            f.write(temp_f.read())
    else:
        # Assume audio_file.file is a path
        with open(audio_file.file, 'wb') as f, open(temp_path, 'rb') as temp_f:
            f.write(temp_f.read())

    # Clean up temporary file
    os.unlink(temp_path)
