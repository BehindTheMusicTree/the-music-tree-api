"""Backward compatibility module for audio_metadata.

This module provides backward compatibility for code that imports from
bodzify_api.utils.audio_metadata. All functionality has been moved to
audiometa_adapter, but this module re-exports everything for compatibility.
"""

METADATA_ARTISTS_SEPARATORS = ["; ", ";", ", ", ","]


def _lazy_import():
    """Lazy import of audiometa_adapter to avoid import errors if audiometa is not installed."""
    from bodzify_api.utils import audiometa_adapter
    return audiometa_adapter


def __getattr__(name):
    """Lazy attribute access for backward compatibility."""
    if name == "METADATA_ARTISTS_SEPARATORS":
        return METADATA_ARTISTS_SEPARATORS
    adapter = _lazy_import()
    return getattr(adapter, name)


__all__ = [
    "METADATA_ARTISTS_SEPARATORS",
    "delete_metadata",
    "delete_potential_id3_metadata_with_header",
    "fix_md5_checking",
    "get_bitrate",
    "get_duration_in_sec",
    "get_merged_app_metadata",
    "get_specific_metadata",
    "is_flac_md5_valid",
    "update_file_metadata",
]
