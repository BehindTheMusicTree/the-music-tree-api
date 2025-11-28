"""Backward compatibility for audio_metadata exceptions."""

from bodzify_api.utils.audiometa_adapter.exceptions import (
    DurationNotFoundError,
    FileByteMismatchError,
    FileCorruptedError,
    FileTypeNotSupportedError,
    FlacMd5CheckFailedError,
    InvalidChunkDecodeError,
    MetadataNotSupportedError,
)

__all__ = [
    "FileCorruptedError",
    "FlacMd5CheckFailedError",
    "FileByteMismatchError",
    "InvalidChunkDecodeError",
    "DurationNotFoundError",
    "FileTypeNotSupportedError",
    "MetadataNotSupportedError",
]


