# Audio Metadata Handling

This module provides audio metadata handling capabilities for the Bodzify API using [`audiometa-python`](https://github.com/your-username/audiometa-python) version 0.2.6.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [Key Components](#key-components)
- [Supported Metadata Fields](#supported-metadata-fields)
- [Supported File Types](#supported-file-types)
- [Usage](#usage)
  - [Reading Metadata](#reading-metadata)
  - [Writing Metadata](#writing-metadata)
    - [Updating Metadata](#updating-metadata)
    - [Deleting Metadata](#deleting-metadata)
  - [Deleting All Metadata](#deleting-all-metadata)
  - [Technical Data](#technical-data)
    - [Audio File Properties](#audio-file-properties)
    - [FLAC-Specific Operations](#flac-specific-operations)
- [Error Handling](#error-handling)
- [Dependencies](#dependencies)
- [Notes](#notes)

## Overview

The `audiometa_adapter` module is a thin adapter layer that:
- Converts Django file types (e.g., `TemporaryUploadedFile`, `FieldFile`) to file paths
- Provides a simplified interface to `audiometa-python` for reading and writing audio metadata
- Handles format-agnostic metadata operations (the library handles format detection automatically)

The underlying `audiometa-python` library is a comprehensive Python library for reading and writing audio metadata across multiple formats including MP3, FLAC, WAV, and more. It supports ID3v1, ID3v2, Vorbis (FLAC), and RIFF (WAV) formats with 15+ metadata fields.

## Architecture

The adapter is **format-agnostic** - it delegates all metadata format decisions (ID3v1, ID3v2, Vorbis, RIFF) to the `audiometa` library. The application doesn't need to know or care about specific metadata formats.

### Key Components

- **`audiometa_adapter`**: Main adapter module providing metadata operations
- **`UnifiedMetadataKey`**: Enum for metadata field names (imported from `audiometa`)
- **`UnifiedMetadata`**: Dictionary type for metadata (imported from `audiometa`)

## Supported Metadata Fields

The adapter supports the following metadata fields (via `UnifiedMetadataKey`):

### Basic Metadata
- `TITLE`: Track title (string)
- `ARTISTS`: List of artist names (list[str])
- `ALBUM`: Album name (string)
- `ALBUM_ARTISTS`: List of album artist names (list[str])
- `GENRES_NAMES`: List of genre names (list[str])
- `RATING`: Rating value (int | float) - supports half-star ratings (e.g., 1.5, 2.5, 3.5)
- `LANGUAGE`: Language code (string)

### Additional Metadata Fields
- `RELEASE_DATE`: Release date (string) - format: YYYY or YYYY-MM-DD
- `TRACK_NUMBER`: Track number (string) - can be int or str format
- `BPM`: Beats per minute (int)
- `COMPOSERS`: List of composer names (list[str])
- `PUBLISHER`: Publisher name (string)
- `COPYRIGHT`: Copyright information (string)
- `UNSYNCHRONIZED_LYRICS`: Lyrics text (string)
- `COMMENT`: Comment text (string)
- `REPLAYGAIN`: ReplayGain value (string)
- `ARCHIVAL_LOCATION`: Archival location (string)

**Note:** Not all metadata fields are supported by all formats. Format-specific limitations apply (e.g., BPM is not supported by RIFF format, album artist is not supported by ID3v1).

## Supported File Types

The adapter accepts the following file types:
- `TemporaryUploadedFile`: Django temporary uploaded file
- `FieldFile`: Django model field file
- `str`: File path string
- `DjangoFile`: Django file object

## Usage

### Reading Metadata

The adapter uses a **merge strategy** for reading metadata (as per the library's default behavior):
- Reads metadata from **all available formats** in the file (ID3v1, ID3v2, Vorbis, RIFF)
- Merges values from multiple formats, with higher-priority formats taking precedence
- Returns a unified metadata dictionary containing the best available values for each field
- When a field exists in multiple formats, the value from the highest-priority format is used

This ensures maximum compatibility and data preservation, as metadata may exist in multiple formats within a single file.

**Format Priority Order:**
- MP3 files: ID3v2 → ID3v1
- FLAC files: Vorbis
- WAV files: RIFF

The library also supports reading from a specific format only (not exposed through the adapter).

```python
from bodzify_api.utils import audiometa_adapter
from audiometa import UnifiedMetadataKey

# Get merged metadata from all available formats
metadata = audiometa_adapter.get_merged_app_metadata(
    file=uploaded_file,
    normalized_rating_max_value=100
)

# Access specific fields
title = metadata.get(UnifiedMetadataKey.TITLE)
artists = metadata.get(UnifiedMetadataKey.ARTISTS)  # List of artist names
genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)  # List of genre names

# Get a specific metadata field
rating = audiometa_adapter.get_specific_metadata(
    file=uploaded_file,
    app_metadata_key=UnifiedMetadataKey.RATING
)
```

### Writing Metadata

The adapter uses an **automatic format selection** strategy for writing metadata (SYNC strategy by default):
- The library automatically selects the most appropriate format based on the file type and existing metadata formats
- For MP3 files: typically writes to ID3v2 tags (defaults to ID3v2.3 for maximum compatibility), but may also write to ID3v1 if present
- For FLAC files: writes to Vorbis comments (the native format for FLAC)
- For WAV files: writes to RIFF tags (the native format for WAV)

**Note:** The actual format(s) used depend on the writing strategy and what metadata formats are already present in the file. The SYNC strategy ensures metadata is synchronized across all formats present in the file.

**Writing Behavior:**

#### Updating Metadata
- **Multiple values (list-type fields)**: For fields that can have multiple values (e.g., `ARTISTS`, `GENRES_NAMES`, `ALBUM_ARTISTS`, `COMPOSERS`), empty strings and `None` values within the list are automatically filtered out before writing. If all values in a list are filtered out, the field is removed entirely (set to `None`)
- **Rating normalization**: Ratings are normalized through star ratings. When `normalized_rating_max_value` is provided, ratings are normalized from a 0-5 star scale (supporting half-stars like 1.5, 2.5, 3.5) to format-specific values. The actual normalized value depends on the target metadata format:
  - **ID3v2 (MP3) and RIFF (WAV)**: Uses a 0-255 non-proportional scale (e.g., 1.5 stars → 54, 3 stars → 128, 5 stars → 255)
  - **Vorbis (FLAC)**: Uses a 0-100 proportional scale (e.g., 1.5 stars → 30, 3 stars → 60, 5 stars → 100)
- **Half-star ratings**: Supports half-star ratings (e.g., 1.5, 2.5, 3.5) for more granular rating systems

#### Deleting Metadata
- **Field removal**: Setting any field to `None` removes that field from the metadata. This works for both single-value fields (e.g., `TITLE`, `ALBUM`) and list-type fields (e.g., `ARTISTS`, `GENRES_NAMES`)

**Note:** The library supports additional writing strategies (PRESERVE, CLEANUP) and format-specific writing, but the adapter uses the default SYNC strategy which ensures metadata is written in the most compatible and feature-rich format for each file type.

```python
from bodzify_api.utils import audiometa_adapter
from audiometa import UnifiedMetadataKey

# Prepare metadata dictionary
metadata = {
    UnifiedMetadataKey.TITLE: "Song Title",
    UnifiedMetadataKey.ARTISTS: ["Artist 1", "Artist 2"],  # List format
    UnifiedMetadataKey.ALBUM: "Album Name",
    UnifiedMetadataKey.ALBUM_ARTISTS: ["Album Artist"],
    UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative"],  # List format
    UnifiedMetadataKey.RATING: 85,
    UnifiedMetadataKey.LANGUAGE: "en"
}

# Update file metadata
audiometa_adapter.update_file_metadata(
    file=uploaded_file,
    app_metadata=metadata,
    normalized_rating_max_value=100
)
```

### Deleting All Metadata

```python
# Delete all metadata from a file
success = audiometa_adapter.delete_metadata(file=uploaded_file)
```

### Technical Data

#### Audio File Properties

```python
# Get bitrate in kbps
bitrate = audiometa_adapter.get_bitrate(file=uploaded_file)

# Get duration in seconds
duration = audiometa_adapter.get_duration_in_sec(file=uploaded_file)
```

#### FLAC-Specific Operations

```python
# Check if FLAC file MD5 checksum is valid
is_valid = audiometa_adapter.is_flac_md5_valid(file=flac_file)

# Fix MD5 checksum and return corrected file
if not is_valid:
    corrected_file = audiometa_adapter.fix_md5_checking(file=flac_file)
    
# Remove ID3 metadata header from FLAC files (if present)
    audiometa_adapter.delete_potential_id3_metadata_with_header(file=flac_file)
```

## Error Handling

All adapter functions handle `FileCorruptedError` exceptions from the `audiometa` library and convert them to the app's `FileCorruptedError` exception. This ensures consistent error handling across the application.

**Note:** The adapter only handles `FileCorruptedError` (the library's custom exception for corrupted files). Other exceptions may also be raised and will propagate:

- **Standard Python exceptions**: `FileNotFoundError`, `PermissionError`, `OSError`, `ValueError`, etc. may be raised from file operations
- **Library exceptions**: The `audiometa` library converts all internal exceptions (including those from underlying dependencies) to its own exception types (e.g., `FileCorruptedError`, `DurationNotFoundError`, `FileByteMismatchError`). Standard I/O exceptions (IOError, OSError, PermissionError) are re-raised as-is, while all other exceptions are converted to `FileCorruptedError`
- **Other exceptions**: Any other exceptions raised by the library or underlying dependencies will propagate unchanged

Callers should be prepared to handle these exceptions as appropriate for their use case.

```python
from bodzify_api.utils.audiometa_adapter.exceptions import FileCorruptedError
from audiometa import UnifiedMetadataKey

# Reading metadata
try:
    metadata = audiometa_adapter.get_merged_app_metadata(file=uploaded_file)
    rating = audiometa_adapter.get_specific_metadata(file=uploaded_file, app_metadata_key=UnifiedMetadataKey.RATING)
except FileCorruptedError as e:
    # Handle corrupted file error
    print(f"File is corrupted: {e}")
except FileNotFoundError as e:
    # Handle file not found error
    print(f"File not found: {e}")
except PermissionError as e:
    # Handle permission error
    print(f"Permission denied: {e}")

# Writing metadata
try:
    audiometa_adapter.update_file_metadata(file=uploaded_file, app_metadata=metadata)
except FileCorruptedError as e:
    # Handle corrupted file error
    print(f"File is corrupted: {e}")

# Technical data operations
try:
    bitrate = audiometa_adapter.get_bitrate(file=uploaded_file)
    duration = audiometa_adapter.get_duration_in_sec(file=uploaded_file)
except FileCorruptedError as e:
    # Handle corrupted file error
    print(f"File is corrupted: {e}")

# FLAC-specific operations
try:
    is_valid = audiometa_adapter.is_flac_md5_valid(file=flac_file)
    if not is_valid:
        corrected_file = audiometa_adapter.fix_md5_checking(file=flac_file)
except FileCorruptedError as e:
    # Handle corrupted file error
    print(f"File is corrupted: {e}")
```

## Dependencies

- `audiometa-python==0.2.6`: Core metadata library
- `mutagen==1.45.0`: Required by audiometa-python for metadata operations

## Notes

- The adapter automatically merges metadata from all available formats in a file
- Format detection and selection is handled by the `audiometa` library
- The application doesn't need to specify metadata formats (ID3v1, ID3v2, Vorbis, RIFF)
- For FLAC files, ID3v2 metadata headers are automatically removed to ensure MD5 checksum validity

