"""Audio file metadata handling module."""

from .audiometa_adapter import (
    delete_metadata,
    fix_md5_checking,
    get_bitrate,
    get_duration_in_sec,
    get_merged_app_metadata,
    get_specific_metadata,
    is_flac_md5_valid,
    update_file_metadata,
)
from .AppMetadataKey import AppMetadataKey
from .exceptions import FileCorruptedError
from .types import AppMetadata, AppMetadataValue

__all__ = [
    "AppMetadata",
    "AppMetadataKey",
    "AppMetadataValue",
    "FileCorruptedError",
    "is_flac_md5_valid",
    "fix_md5_checking",
    "get_bitrate",
    "get_duration_in_sec",
    "get_merged_app_metadata",
    "get_specific_metadata",
    "update_file_metadata",
    "delete_metadata",
]
