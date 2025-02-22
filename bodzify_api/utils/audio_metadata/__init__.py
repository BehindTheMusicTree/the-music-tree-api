
from .audio_file import AudioFile
import shutil
import tempfile
import os
import subprocess
from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db.models.fields.files import FieldFile

from bodzify_api.utils.audio_metadata.exceptions import FileByteMismatchError, FlacMd5CheckFailedError, InvalidChunkDecodeError

from .id3.Mp3MetadataManager import Mp3MetadataManager
from .id3.WavMetadataManager import WavMetadataManager
from .MetadataManager import MetadataManager
from mutagen._file import File as MutagenFile
from .vorbis.VorbisManager import VorbisManager
from .flac_id3v2.FlacID3v2Manager import FlacID3v2Manager


FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."


def create_temporary_copy(file) -> AudioFile:
    return AudioFile(file)


def _get_metadata_manager(file, use_id3v2: bool = False) -> MetadataManager:
    temp_file = create_temporary_copy(file)
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == ".mp3":
        return Mp3MetadataManager(temp_file)
    elif file_extension == ".wav":
        return WavMetadataManager(temp_file)
    elif file_extension == ".flac":
        if use_id3v2:
            return FlacID3v2Manager(temp_file)
        else:
            return VorbisManager(temp_file)
    else:
        raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)


def is_md5_valid(file, use_id3v2: bool = False):
    return _get_metadata_manager(file, use_id3v2=use_id3v2).is_md5_valid()


def get_bitrate_from_file(file):
    return _get_metadata_manager(file).get_bitrate()


def get_specific_metadata_from_file(file, normalized_metadata_key: str, use_id3v2: bool = False):
    return _get_metadata_manager(
        file, use_id3v2=use_id3v2).get_specific_file_metadata(
        normalized_metadata_key=normalized_metadata_key)


def get_raw_metadata_from_file(file, use_id3v2: bool = False) -> dict:
    return _get_metadata_manager(file=file, use_id3v2=use_id3v2).file_metadata


def get_normalized_metadata_from_file(
        file, normalized_rating_max_value: Optional[int] = None, use_id3v2: bool = False) -> dict:
    try:
        return _get_metadata_manager(file, use_id3v2=use_id3v2).get_normalized_metadata(normalized_rating_max_value)
    except Exception as error:
        error_str = str(error)
        if "file said" in error_str and "bytes, read" in error_str:
            raise FileByteMismatchError(error_str.capitalize())
        elif "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
            raise InvalidChunkDecodeError(error_str)
        raise


def update_file_metadata(file, normalized_metadata: dict, normalized_rating_max_value: int):
    _get_metadata_manager(file).update_file_metadata(normalized_metadata=normalized_metadata,
                                                     normalized_rating_max_value=normalized_rating_max_value)


def replace_flac_file_with_corrected_md5(file_obj):
    if isinstance(file_obj, str):
        result = subprocess.run(['flac', '-f', '--best', file_obj], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif isinstance(file_obj, InMemoryUploadedFile):
        file_obj.seek(0)  # Ensure we're at the start of the file
        # Create a temporary file for the corrected output
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.flac', delete=False) as temp_file:
            temp_path = temp_file.name
            # Run FLAC and save to temporary file
            result = subprocess.run(
                ['flac', '-f', '--best', '-o', temp_path, '-'],
                input=file_obj.read(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stderr = result.stderr.decode()
            if 'wrote' not in stderr:
                os.unlink(temp_path)  # Clean up temp file
                raise FlacMd5CheckFailedError(
                    "The Flac file md5 check failed and could not be corrected. The file is probably corrupted.")

            # Replace original file content with corrected content
            file_obj.seek(0)
            with open(temp_path, 'rb') as f:
                file_obj.write(f.read())
            file_obj.truncate()

            # Clean up
            os.unlink(temp_path)
    else:
        raise ImproperlyConfigured("Expected string path or InMemoryUploadedFile")
