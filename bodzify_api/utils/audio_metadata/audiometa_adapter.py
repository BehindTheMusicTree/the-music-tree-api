"""Audio metadata handling module.

This module provides a backward-compatible wrapper around audiometa-python 0.2.4.
"""

import os

import audiometa
from audiometa import UnifiedMetadata, UnifiedMetadataKey
from audiometa.exceptions import FileCorruptedError as AudiometaFileCorruptedError
from audiometa.utils.metadata_format import MetadataFormat as AudiometaMetadataFormat
from audiometa.utils.flac_md5_state import FlacMd5State
from django.core.files import File as DjangoFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile

from bodzify_api.utils.file_path_utils import get_file_path as _get_file_path_util
from .types import AppMetadata, AppMetadataValue
from .AppMetadataKey import AppMetadataKey
from .exceptions import FileCorruptedError

MetadataFormat = AudiometaMetadataFormat

FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."

FILE_TYPE = TemporaryUploadedFile | FieldFile | str | DjangoFile

_APP_TO_UNIFIED_KEY_MAP = {
    AppMetadataKey.TITLE: UnifiedMetadataKey.TITLE,
    AppMetadataKey.ARTISTS_NAMES: UnifiedMetadataKey.ARTISTS,
    AppMetadataKey.ALBUM_NAME: UnifiedMetadataKey.ALBUM,
    AppMetadataKey.ALBUM_ARTISTS_NAMES: UnifiedMetadataKey.ALBUM_ARTISTS,
    AppMetadataKey.GENRE_NAME: UnifiedMetadataKey.GENRES_NAMES,
    AppMetadataKey.RATING: UnifiedMetadataKey.RATING,
    AppMetadataKey.LANGUAGE: UnifiedMetadataKey.LANGUAGE,
}

_UNIFIED_TO_APP_KEY_MAP = {v: k for k, v in _APP_TO_UNIFIED_KEY_MAP.items()}


def _convert_unified_to_app_metadata(unified_metadata: UnifiedMetadata) -> AppMetadata:
    """Convert UnifiedMetadata to AppMetadata."""
    app_metadata: AppMetadata = {}
    for unified_key, value in unified_metadata.items():
        if unified_key in _UNIFIED_TO_APP_KEY_MAP:
            app_key = _UNIFIED_TO_APP_KEY_MAP[unified_key]
            if app_key == AppMetadataKey.GENRE_NAME:
                if isinstance(value, list) and len(value) > 0:
                    app_metadata[app_key] = value[0]
                elif isinstance(value, str):
                    app_metadata[app_key] = value
            else:
                app_metadata[app_key] = value
    return app_metadata


def _convert_app_to_unified_metadata(app_metadata: AppMetadata) -> dict:
    """Convert AppMetadata to UnifiedMetadata."""
    unified_metadata: dict = {}
    for app_key, value in app_metadata.items():
        if app_key in _APP_TO_UNIFIED_KEY_MAP:
            unified_key = _APP_TO_UNIFIED_KEY_MAP[app_key]
            if app_key in (AppMetadataKey.GENRE_NAME, AppMetadataKey.ARTISTS_NAMES, AppMetadataKey.ALBUM_ARTISTS_NAMES):
                if value is None:
                    # Explicitly set to None to delete the metadata field
                    unified_metadata[unified_key] = None
                elif isinstance(value, str):
                    # Skip empty strings - they should delete the metadata field
                    if value:
                        unified_metadata[unified_key] = [value]
                    else:
                        unified_metadata[unified_key] = None
                elif isinstance(value, list):
                    unified_metadata[unified_key] = value
            else:
                # Convert empty strings to None for non-list fields
                unified_metadata[unified_key] = value if value != "" else None

    return unified_metadata


def get_merged_app_metadata(file: FILE_TYPE, normalized_rating_max_value: int | None = None) -> AppMetadata:
    """Get merged metadata from all available formats."""
    file_path = _get_file_path_util(file)
    try:
        unified_metadata = audiometa.get_unified_metadata(
            file=file_path, normalized_rating_max_value=normalized_rating_max_value
        )
    except AudiometaFileCorruptedError as e:
        raise FileCorruptedError(str(e)) from e
    return _convert_unified_to_app_metadata(unified_metadata)


def get_specific_metadata(file: FILE_TYPE, app_metadata_key: AppMetadataKey) -> AppMetadataValue:
    """Get a specific metadata field."""
    file_path = _get_file_path_util(file)
    unified_key = _APP_TO_UNIFIED_KEY_MAP.get(app_metadata_key)
    if not unified_key:
        return None
    value = audiometa.get_unified_metadata_field(file=file_path, unified_metadata_key=unified_key)
    if app_metadata_key == AppMetadataKey.GENRE_NAME and isinstance(value, list) and len(value) > 0:
        return value[0]
    return value


def update_file_metadata(
    file: FILE_TYPE, app_metadata: AppMetadata, normalized_rating_max_value: int | None = None
) -> None:
    """Update metadata in a file."""
    file_path = _get_file_path_util(file)
    unified_metadata = _convert_app_to_unified_metadata(app_metadata)

    audiometa.update_metadata(
        file=file_path,
        unified_metadata=unified_metadata,
        normalized_rating_max_value=normalized_rating_max_value,
        warn_on_unsupported_field=False,
    )


def delete_metadata(file: FILE_TYPE, tag_format: MetadataFormat | None = None) -> bool:
    """Delete metadata from a file."""
    file_path = _get_file_path_util(file)
    return audiometa.delete_all_metadata(file=file_path, metadata_format=tag_format)


def get_bitrate(file: FILE_TYPE) -> int:
    """Get bitrate in kbps."""
    file_path = _get_file_path_util(file)
    try:
        return audiometa.get_bitrate(file=file_path) // 1000
    except AudiometaFileCorruptedError as e:
        raise FileCorruptedError(str(e)) from e


def get_duration_in_sec(file: FILE_TYPE) -> float:
    """Get duration in seconds."""
    file_path = _get_file_path_util(file)
    try:
        return audiometa.get_duration_in_sec(file=file_path)
    except AudiometaFileCorruptedError as e:
        raise FileCorruptedError(str(e)) from e


def is_flac_md5_valid(file: FILE_TYPE) -> bool:
    """Check if FLAC file MD5 is valid."""
    file_path = _get_file_path_util(file)
    try:
        md5_validation_result = audiometa.is_flac_md5_valid(file=file_path)
        # audiometa.is_flac_md5_valid returns an enum, convert to bool
        return md5_validation_result == FlacMd5State.VALID
    except AudiometaFileCorruptedError as e:
        raise FileCorruptedError(str(e)) from e


def fix_md5_checking(file: FILE_TYPE) -> TemporaryUploadedFile:
    """Return a temporary file with corrected MD5 signature."""
    file_path = _get_file_path_util(file)
    fixed_path = audiometa.fix_md5_checking(file=file_path)
    file_size = os.path.getsize(fixed_path)
    md5_validation_result = audiometa.is_flac_md5_valid(file=fixed_path)
    # audiometa.is_flac_md5_valid returns an enum, not a bool
    # Compare against the enum value that represents valid
    if md5_validation_result != FlacMd5State.VALID:
        os.unlink(fixed_path)
        error_message = f"MD5 correction failed - the corrected file has MD5 validation result: {md5_validation_result} (expected {FlacMd5State.VALID})"
        raise FileCorruptedError(error_message)
    temp_uploaded = TemporaryUploadedFile(
        name=os.path.basename(fixed_path),
        content_type="audio/flac",
        size=file_size,
        charset=None,
    )
    temp_file_path = temp_uploaded.temporary_file_path()
    os.rename(fixed_path, temp_file_path)
    with open(temp_file_path, 'rb') as f:
        f.read(1)
        f.seek(0)
    return temp_uploaded
