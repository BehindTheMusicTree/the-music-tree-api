
from .audio_file import AudioFile
import tempfile
import os
import subprocess
from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile

from bodzify_api.utils.audio_metadata.exceptions import FileByteMismatchError, FlacMd5CheckFailedError, InvalidChunkDecodeError

from .id3.Mp3MetadataManager import Mp3MetadataManager
from .id3.WavMetadataManager import WavMetadataManager
from .MetadataManager import MetadataManager
from mutagen._file import File as MutagenFile
from .vorbis.VorbisManager import VorbisManager
from .flac_id3v2.FlacID3v2Manager import FlacID3v2Manager


FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."


def _get_metadata_manager(file, tag_types: Optional[list[str]] = None) -> dict[str, MetadataManager]:
    """Get metadata managers for specified tag types.

    Args:
        file: The audio file to analyze
        tag_types: List of tag types to extract. Supported values: ['id3v2', 'vorbis', 'riff']
                  If None, returns default manager for the file type.

    Returns:
        Dict mapping tag type to corresponding MetadataManager instance
    """
    audio_file = AudioFile(file)
    managers = {}

    if tag_types is None:
        # Default behavior - single manager
        if audio_file.file_extension == ".mp3":
            managers['id3v2'] = Mp3MetadataManager(audio_file)
        elif audio_file.file_extension == ".wav":
            managers['riff'] = WavMetadataManager(audio_file)
        elif audio_file.file_extension == ".flac":
            managers['vorbis'] = VorbisManager(audio_file)
        else:
            raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)
        return managers

    # Multiple tag types requested
    for tag_type in tag_types:
        if tag_type == 'id3v2':
            if audio_file.file_extension in [".mp3", ".flac"]:
                managers['id3v2'] = Mp3MetadataManager(
                    audio_file) if audio_file.file_extension == ".mp3" else FlacID3v2Manager(audio_file)
        elif tag_type == 'vorbis' and audio_file.file_extension == ".flac":
            managers['vorbis'] = VorbisManager(audio_file)
        elif tag_type == 'riff' and audio_file.file_extension == ".wav":
            managers['riff'] = WavMetadataManager(audio_file)

    if not managers:
        raise ImproperlyConfigured(
            f"No supported tag types ({', '.join(tag_types)}) for file extension {audio_file.file_extension}")

    return managers


def is_md5_valid(file, check_id3v2: bool = False):
    audio_file = AudioFile(file)

    if audio_file.file_extension == ".flac":
        if check_id3v2:
            id3v2_tags = FlacID3v2Manager(audio_file).file_raw_metadata
            if id3v2_tags:
                return False
        return audio_file.is_flac_file_md5_valid()
    else:
        raise ImproperlyConfigured('The file must be a FLAC file to check the MD5.')


def get_bitrate_from_file(file):
    # Use default manager for bitrate
    manager = next(iter(_get_metadata_manager(AudioFile(file)).values()))
    return manager.get_bitrate()


def get_specific_metadata_from_file(file, normalized_metadata_key: str, tag_types: Optional[list[str]] = None):
    """Get specific metadata from file using specified tag types.
    If tag_types is None, uses default manager for the file type."""
    managers = _get_metadata_manager(file, tag_types=tag_types)
    results = {}
    for tag_type, manager in managers.items():
        results[tag_type] = manager.get_specific_file_metadata(normalized_metadata_key=normalized_metadata_key)
    return results


def get_raw_metadata_from_file(file, tag_types: Optional[list[str]] = None) -> dict:
    """Get raw metadata from file using specified tag types.
    If tag_types is None, uses default manager for the file type."""
    managers = _get_metadata_manager(file, tag_types=tag_types)
    results = {}
    for tag_type, manager in managers.items():
        results[tag_type] = manager.file_raw_metadata
    return results


def get_normalized_metadata_from_file(
        file, normalized_rating_max_value: Optional[int] = None, tag_types: Optional[list[str]] = None) -> dict[str, dict]:
    """Get normalized metadata from specified tag types.

    Args:
        file: The audio file to analyze
        normalized_rating_max_value: Optional max value for normalizing ratings
        tag_types: List of tag types to extract. Supported: ['id3v2', 'vorbis', 'riff']
                  If None, returns metadata from default tag type for the file.

    Returns:
        Dict mapping tag type to normalized metadata dict for that format
    """
    try:
        managers = _get_metadata_manager(file, tag_types=tag_types)
        metadata = {}

        for tag_type, manager in managers.items():
            metadata[tag_type] = manager.get_normalized_metadata(normalized_rating_max_value)

        return metadata

    except Exception as error:
        error_str = str(error)
        if "file said" in error_str and "bytes, read" in error_str:
            raise FileByteMismatchError(error_str.capitalize())
        elif "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
            raise InvalidChunkDecodeError(error_str)
        raise


def update_file_metadata(file, normalized_metadata: dict, normalized_rating_max_value: int):
    # Use default manager for updates
    manager = next(iter(_get_metadata_manager(file).values()))
    manager.update_file_metadata(normalized_metadata=normalized_metadata,
                                 normalized_rating_max_value=normalized_rating_max_value)


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
