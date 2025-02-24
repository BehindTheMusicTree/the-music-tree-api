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

from bodzify_api.utils.audio_metadata.AppMetadataKeys import AppMetadataKeys
from bodzify_api.utils.audio_metadata.manager.vorbis.VorbisManager import VorbisManager
from .audio_file import AudioFile
import tempfile
import os
import subprocess
from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile

from bodzify_api.utils.audio_metadata.exceptions import FileByteMismatchError, FlacMd5CheckFailedError, InvalidChunkDecodeError

from .manager.id3.Id3v2Manager import Id3v2Manager
from .manager.id3.Id3v1Manager import Id3v1Manager
from .manager.riff.RiffManager import RiffManager
from .manager.MetadataManager import MetadataManager


from .tag_types import TagTypes

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."


def _get_metadata_manager(file, tag_types: Optional[list[TagTypes]] = None) -> dict[str, MetadataManager]:
    """
    Args:
        file: The audio file to analyze
        tag_types: List of tag types to extract. Use TagTypes enum values.
                  If None, returns default manager for the file type.

    Returns:
        Dict mapping tag type to corresponding MetadataManager instance
    """
    audio_file = AudioFile(file)
    managers = {}

    if tag_types is None:
        # Default behavior - single manager
        if audio_file.file_extension == ".mp3":
            managers[TagTypes.ID3V2] = Id3v2Manager(audio_file)
        elif audio_file.file_extension == ".wav":
            managers[TagTypes.RIFF] = RiffManager(audio_file)
        elif audio_file.file_extension == ".flac":
            managers[TagTypes.VORBIS] = VorbisManager(audio_file)
        else:
            raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
        return managers

    # Multiple tag types requested
    for tag_type in tag_types:
        if tag_type == TagTypes.ID3V2 and audio_file.file_extension in [".mp3", ".flac"]:
            managers[TagTypes.ID3V2] = Id3v2Manager(audio_file)
        elif tag_type == TagTypes.VORBIS and audio_file.file_extension == ".flac":
            managers[TagTypes.VORBIS] = VorbisManager(audio_file)
        elif tag_type == TagTypes.RIFF and audio_file.file_extension == ".wav":
            managers[TagTypes.RIFF] = RiffManager(audio_file)
        elif tag_type == TagTypes.ID3V1 and audio_file.file_extension == ".mp3":
            managers[TagTypes.ID3V1] = Id3v1Manager(audio_file)

    if not managers:
        raise ImproperlyConfigured(
            f"No supported tag types ({', '.join(tag_types)}) for file extension {audio_file.file_extension}")

    return managers


def is_md5_valid(file, check_id3v2: bool = False):
    audio_file = AudioFile(file)

    if audio_file.file_extension == ".flac":
        if check_id3v2:
            id3v2_tags = Id3v2Manager(audio_file).file_raw_metadata
            if id3v2_tags:
                return False
        return audio_file.is_flac_file_md5_valid()
    else:
        raise ImproperlyConfigured('The file must be a FLAC file to check the MD5.')


def get_bitrate_from_file(file):
    """Get bitrate in kbps from audio file.

    Args:
        file: Audio file to get bitrate from

    Returns:
        int: Bitrate in kbps, or 0 if bitrate cannot be determined
    """
    audio_file = AudioFile(file)
    return audio_file.get_bitrate()


def get_specific_metadata_from_file(file, app_metadata_key: str, tag_types: Optional[list[TagTypes]] = None):
    """Get specific metadata from file using specified tag types.
    If tag_types is None, uses default manager for the file type.

    Args:
        file: The audio file to analyze
        app_metadata_key: The metadata key to extract
        tag_types: List of TagTypes enum values to extract from
    """
    managers = _get_metadata_manager(file, tag_types=tag_types)
    results = {}
    for tag_type, manager in managers.items():
        results[tag_type] = manager.get_specific_file_metadata(app_metadata_key=app_metadata_key)
    return results


def get_raw_metadata_from_file(file, tag_types: Optional[list[TagTypes]] = None) -> dict:
    managers = _get_metadata_manager(file, tag_types=tag_types)
    results = {}
    for tag_type, manager in managers.items():
        results[tag_type] = manager.file_raw_metadata
    return results


def get_normalized_metadata_from_file(
        file,
        normalized_rating_max_value: Optional[int] = None,
        tag_types: Optional[list[TagTypes]] = None,
        merge_tags: bool = False) -> dict[str, dict]:
    """Get normalized metadata from specified tag types.

    Args:
        file: The audio file to analyze
        normalized_rating_max_value: Optional max value for normalizing ratings
        tag_types: List of TagTypes enum values to extract from.
                  If None, returns metadata from default tag type for the file.
        merge_tags: If True, includes a 'merged' key with metadata merged according to tag priorities

    Returns:
        Dict mapping tag type to normalized metadata dict for that format.
        If merge_tags is True, includes a 'merged' key with prioritized metadata.
    """
    try:
        managers = _get_metadata_manager(file, tag_types=tag_types)
        metadata = {}

        for tag_type, manager in managers.items():
            try:
                metadata[tag_type] = manager.get_normalized_metadata(normalized_rating_max_value)
            except Exception as e:
                metadata[tag_type] = {"error": str(e)}

        if merge_tags:
            return get_merged_metadata(metadata, AudioFile(file).file_extension)
        return metadata

    except Exception as error:
        error_str = str(error)
        if "file said" in error_str and "bytes, read" in error_str:
            raise FileByteMismatchError(error_str.capitalize())
        elif "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
            raise InvalidChunkDecodeError(error_str)
        raise


def get_merged_metadata(metadata: dict[str, dict], file_extension: str) -> dict[str, dict]:
    """Merge metadata from different tag types with priority ordering.

    The priority order is defined in TAG_TYPE_PRIORITIES. For each metadata field,
    the function tries tag types in priority order and uses the first valid value found.

    Example for FLAC files:
    If both Vorbis and ID3v2 tags contain a title, the Vorbis title is used.
    If Vorbis tags don't have a title but ID3v2 does, the ID3v2 title is used.

    Args:
        metadata: Dictionary of metadata by tag type
        file_extension: File extension to determine priority order

    Returns:
        Dictionary with merged metadata under 'merged' key, plus original tag data
    """
    priorities = TagTypes.get_priorities().get(file_extension.lower(), [])
    if not priorities:
        raise ImproperlyConfigured(f"No priority order defined for {file_extension}")

    # Start with empty merged metadata
    merged = {}

    # For each field that could exist in metadata
    for field in vars(AppMetadataKeys).values():
        if not isinstance(field, str) or field.startswith('_'):
            continue

        # Try each tag type in priority order
        for tag_type in priorities:
            if (tag_type in metadata and
                isinstance(metadata[tag_type], dict) and
                "error" not in metadata[tag_type] and
                field in metadata[tag_type] and
                    metadata[tag_type][field] is not None):
                merged[field] = metadata[tag_type][field]
                break

    # Add merged result while preserving original tag data
    metadata['merged'] = merged
    return metadata


def get_prioritized_metadata_from_file(
        file, normalized_rating_max_value: Optional[int] = None) -> dict:
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
    tag_types = TagTypes.get_priorities().get(audio_file.file_extension.lower())

    if not tag_types:
        raise ImproperlyConfigured(f"File type {audio_file.file_extension} not supported")

    # Get metadata from all relevant tag types and merge with priority
    metadata = get_normalized_metadata_from_file(
        file,
        normalized_rating_max_value=normalized_rating_max_value,
        tag_types=tag_types,
        merge_tags=True
    )

    return metadata['merged']


def update_file_metadata(file, normalized_metadata: dict, normalized_rating_max_value: int):
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
    priorities = TagTypes.get_priorities().get(audio_file.file_extension.lower())
    if not priorities:
        raise ImproperlyConfigured(f"File type {audio_file.file_extension} not supported")

    # Get the highest priority tag type for this format
    primary_tag_type = priorities[0]

    # Get the manager for just this tag type
    managers = _get_metadata_manager(file, tag_types=[primary_tag_type])
    if not managers or primary_tag_type not in managers:
        raise ImproperlyConfigured(
            f"Could not get {primary_tag_type} manager for {audio_file.file_extension}")

    # Use the primary manager for updates
    managers[primary_tag_type].update_file_metadata(
        normalized_metadata=normalized_metadata,
        normalized_rating_max_value=normalized_rating_max_value)


def delete_metadata(file, tag_types: Optional[list[TagTypes]] = None) -> dict[TagTypes, bool]:
    managers = _get_metadata_manager(file, tag_types=tag_types)
    results = {}
    for tag_type, manager in managers.items():
        results[tag_type] = manager.delete_metadata()
    return results


def replace_flac_file_with_corrected_md5(file):
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
