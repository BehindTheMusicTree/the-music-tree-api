
import os
import subprocess
from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from bodzify_api.utils.audio_metadata.exceptions import FlacFileProbablyCorruptedError

from .id3.Mp3MetadataManager import Mp3MetadataManager
from .id3.WavMetadataManager import WavMetadataManager
from .MetadataManager import MetadataManager
from .vorbis.VorbisManager import VorbisManager

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."


def get_bitrate_from_file(file):
    return _get_metadata_manager(file).get_bitrate()


def get_specific_metadata_from_file(file, normalized_metadata_key: str):
    return _get_metadata_manager(file).get_specific_file_metadata(normalized_metadata_key=normalized_metadata_key)


def get_normalized_metadata_from_file(file, normalized_rating_max_value: Optional[int] = None) -> dict:
    return _get_metadata_manager(file).get_normalized_metadata(normalized_rating_max_value)


def _get_metadata_manager(file) -> MetadataManager:
    if hasattr(file, 'name'):
        _, file_extension = os.path.splitext(file.name)
    else:
        _, file_extension = os.path.splitext(file)
    file_extension_lowered = file_extension.lower()
    if file_extension_lowered == ".mp3":
        return Mp3MetadataManager(file)
    elif file_extension_lowered == ".wav":
        return WavMetadataManager(file)
    elif file_extension_lowered == ".flac":
        return VorbisManager(file)
    else:
        raise ImproperlyConfigured(FILE_EXTENSION_NOT_HANDLED_MESSAGE)


def update_file_metadata(file, normalized_metadata: dict, normalized_rating_max_value: int):
    _get_metadata_manager(file).update_file_metadata(normalized_metadata=normalized_metadata,
                                                     normalized_rating_max_value=normalized_rating_max_value)


def is_flac_file_md5_valid(file_obj):
    if isinstance(file_obj, str):
        result = subprocess.run(['flac', '-t', file_obj], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif isinstance(file_obj, InMemoryUploadedFile):
        file_obj.seek(0)  # Ensure we're at the start of the file
        result = subprocess.run(
            ['flac', '-t', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=file_obj.read())
    elif isinstance(file_obj, TemporaryUploadedFile):
        result = subprocess.run(['flac', '-t', file_obj.temporary_file_path()],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        raise ImproperlyConfigured("Expected string path or InMemoryUploadedFile")

    output = result.stderr.decode()
    if 'ok' in output:
        return True
    if 'MD5 signature mismatch' in output:
        return False
    else:
        raise Exception("The Flac file md5 check failed")


def replace_flac_file_with_corrected_md5(file_obj):
    if isinstance(file_obj, str):
        result = subprocess.run(['flac', '-f', '--best', file_obj], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif isinstance(file_obj, InMemoryUploadedFile):
        file_obj.seek(0)  # Ensure we're at the start of the file
        result = subprocess.run(
            ['flac', '-f', '--best', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=file_obj.read())

    stderr = result.stderr.decode()
    if 'wrote' not in stderr:
        raise FlacFileProbablyCorruptedError(
            "The Flac file md5 check failed and could not be corrected. The file is probably corrupted.")
