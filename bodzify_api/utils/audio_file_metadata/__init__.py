"""Audio file metadata handling module."""

from .audiometa_adapter import (
    get_merged_app_metadata,
    get_specific_metadata,
    get_full_metadata,
    delete_metadata,
    update_file_metadata,
    get_bitrate,
    get_duration_in_sec,
    is_flac_md5_valid,
    fix_md5_checking,
)
from .AppMetadataKey import AppMetadataKey
from .exceptions import FileCorruptedError
from .types import AppMetadata, AppMetadataValue

__all__ = [
    "AppMetadata",
    "AppMetadataKey",
    "AppMetadataValue",
    "FileCorruptedError",
    "get_specific_metadata",
    "get_merged_app_metadata",
    "get_full_metadata",
    "update_file_metadata",
    "delete_metadata",
    "get_bitrate",
    "get_duration_in_sec",
    "is_flac_md5_valid",
    "fix_md5_checking",
]
