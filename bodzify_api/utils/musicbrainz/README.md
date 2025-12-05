# MusicBrainz Integration for Bodzify API

This module provides integration with MusicBrainz through the AcoustID fingerprinting service, allowing the application to identify audio tracks and retrieve metadata such as title, artist, release date, and more.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
  - [1. Install Dependencies](#1-install-dependencies)
  - [2. Get an AcoustID API Key](#2-get-an-acoustid-api-key)
  - [3. Configure AcoustID API Key](#3-configure-acoustid-api-key)
  - [4. Run Migrations](#4-run-migrations)
- [How It Works](#how-it-works)
  - [Audio Fingerprinting Flow](#audio-fingerprinting-flow)
  - [Recording Selection Algorithm](#recording-selection-algorithm)
- [Usage](#usage)
  - [Looking Up a Recording by Fingerprint](#looking-up-a-recording-by-fingerprint)
  - [Creating or Updating a Recording from API Response](#creating-or-updating-a-recording-from-api-response)
- [Response Structure](#response-structure)
  - [AcoustID API Response](#acoustid-api-response)
  - [Recording Dictionary Structure](#recording-dictionary-structure)
  - [MusicbrainzRecordingLookupResult](#musicbrainzrecordinglookupresult)
  - [MusicbrainzRecording Model](#musicbrainzrecording-model)
  - [MbRecordingMissingCause Model](#mbrecordingmissingcause-model)
- [Error Handling](#error-handling)
- [Models](#models)
- [Testing](#testing)
- [References](#references)

## Overview

The MusicBrainz integration uses audio fingerprinting to identify tracks:

1. **Audio Fingerprinting**: Audio files are fingerprinted using Chromaprint
2. **AcoustID Lookup**: Fingerprints are sent to the AcoustID web service to find matching recordings
3. **MusicBrainz Metadata**: AcoustID returns MusicBrainz recording IDs, which are used to retrieve detailed metadata
4. **Database Storage**: Recording metadata is stored locally and updated when the same track is identified again

## Setup

### 1. Install Dependencies

The MusicBrainz integration requires the `pyacoustid` library. Make sure it's installed:

```
pip install -r requirements.txt
```

### 2. Get an AcoustID API Key

The integration uses the [AcoustID Web Service](https://acoustid.org/webservice) to look up audio fingerprints. You need to obtain a free API key:

1. Visit the [AcoustID Web Service](https://acoustid.org/webservice)
2. Sign up for a free account
3. Generate an API key from your account dashboard

### 3. Configure AcoustID API Key

Set the following environment variable with your AcoustID API key:

```
ACOUSTID_API_KEY=your_acoustid_api_key
```

### 4. Run Migrations

Ensure the MusicBrainz models are migrated to your database:

```
python manage.py makemigrations
python manage.py migrate
```

## How It Works

### Audio Fingerprinting Flow

```
Audio File → Chromaprint Fingerprint → AcoustID API → MusicBrainz Recording → Database
```

1. When an audio file is uploaded, it's fingerprinted using Chromaprint
2. The fingerprint and duration are sent to the AcoustID web service
3. AcoustID matches the fingerprint to MusicBrainz recordings
4. The best matching recording is selected based on:
   - Score (confidence level)
   - Duration similarity
   - Number of available metadata fields
   - Number of release groups
5. Recording metadata is stored in the database and associated with the track

### Recording Selection Algorithm

When multiple recordings match a fingerprint, the system selects the best one using this algorithm:

1. **Group by score**: Recordings are grouped by their AcoustID confidence score
2. **Select highest score group**: The group with the highest score is chosen
3. **Rank within group**: Within that group, recordings are ranked by:
   - Duration difference (closer is better)
   - Number of metadata fields (more is better)
   - Number of release groups (more is better)

## Usage

### Looking Up a Recording by Fingerprint

The main entry point is `get_musicbrainz_recording_lookup_result()`:

```python
from bodzify_api.utils.musicbrainz.service import get_musicbrainz_recording_lookup_result
from bodzify_api.model.user.User import User

# Get fingerprint from audio file (using chromaprint)
fingerprint = get_audio_fingerprint(audio_file_path)
duration_in_sec = 180.5  # Track duration in seconds
user = User.objects.get(id=1)

# Look up the recording
result = get_musicbrainz_recording_lookup_result(
    user=user,
    fingerprint=fingerprint,
    duration_in_sec=duration_in_sec
)

if result.is_success:
    recording = result.recording
    print(f"Title: {recording.title}")
    print(f"Artists: {recording.musicbrainz_artists.all()}")
    print(f"Duration: {recording.duration_str_in_hour_min_sec}")
    print(f"Release Date: {recording.release_date}")
    print(f"MusicBrainz Link: {recording.musicbrainz_link}")
else:
    missing_cause = result.missing_cause
    print(f"Lookup failed: {missing_cause.code.code}")
    if missing_cause.message:
        print(f"Error: {missing_cause.message}")
```

### Creating or Updating a Recording from API Response

If you already have a MusicBrainz recording dictionary (from API response), you can create or update the database record:

```python
from bodzify_api.utils.musicbrainz.utils import create_or_update_musicbrainz_recording_instance_from_dict
from bodzify_api.utils.musicbrainz.ApiFields import ApiFields

recording_dict = {
    ApiFields.Names.ID: "4a45b00b-273d-40ed-9ecd-42f387f59c22",
    ApiFields.Names.TITLE: "Drown (Massano remix)",
    ApiFields.Names.SCORE: 0.95,
    ApiFields.Names.DURATION_IN_SEC: 440,
    ApiFields.Names.ARTISTS: [
        {ApiFields.Names.ID: "artist-1", ApiFields.Names.NAME: "Artist Name"}
    ],
    ApiFields.Names.RELEASEGROUPS: []
}

recording = create_or_update_musicbrainz_recording_instance_from_dict(
    musicbrainz_recording_id=recording_dict[ApiFields.Names.ID],
    musicbrainz_recording_dict=recording_dict
)
```

**Note**: This function will:
- Create a new recording if it doesn't exist
- Update existing recording fields (title, score, duration, release date) if it already exists
- Create or update associated artists

## Response Structure

### AcoustID API Response

The AcoustID API returns a response with the following structure:

```json
{
  "status": "ok",
  "results": [
    {
      "score": 0.95,
      "recordings": [
        {
          "id": "4a45b00b-273d-40ed-9ecd-42f387f59c22",
          "title": "Drown (Massano remix)",
          "duration": 440,
          "artists": [
            {
              "id": "artist-mb-id-1",
              "name": "Artist Name"
            }
          ],
          "releasegroups": [
            {
              "releases": [
                {
                  "date": {
                    "year": 2023,
                    "month": 6,
                    "day": 15
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Error Response:**

```json
{
  "status": "error",
  "error": {
    "code": 3,
    "message": "Invalid fingerprint"
  }
}
```

### Recording Dictionary Structure

The recording dictionary extracted from the AcoustID response has the following structure:

```python
recording_dict = {
    "id": "4a45b00b-273d-40ed-9ecd-42f387f59c22",  # MusicBrainz recording ID (required)
    "title": "Drown (Massano remix)",              # Recording title (required)
    "score": 0.95,                                  # Confidence score 0.0-1.0 (required)
    "duration": 440,                                # Duration in seconds (optional)
    "artists": [                                    # List of artists (required)
        {
            "id": "artist-mb-id-1",                 # MusicBrainz artist ID (required)
            "name": "Artist Name"                    # Artist name (required)
        }
    ],
    "releasegroups": [                              # List of release groups (optional)
        {
            "releases": [                           # List of releases (optional)
                {
                    "date": {                       # Release date (optional)
                        "year": 2023,              # Year (required if date present)
                        "month": 6,                 # Month 1-12 (optional)
                        "day": 15                   # Day 1-31 (optional)
                    }
                }
            ]
        }
    ]
}
```

**Field Descriptions:**

- `id` (string, required): MusicBrainz recording UUID
- `title` (string, required): Recording title
- `score` (float, required): Confidence score from AcoustID (0.0 to 1.0)
- `duration` (integer, optional): Duration in seconds
- `artists` (list, required): List of artist dictionaries, each containing:
  - `id` (string, required): MusicBrainz artist UUID
  - `name` (string, required): Artist name
- `releasegroups` (list, optional): List of release group dictionaries, each containing:
  - `releases` (list, optional): List of release dictionaries, each containing:
    - `date` (dict, optional): Release date with `year`, `month`, `day` fields

### MusicbrainzRecordingLookupResult

The `get_musicbrainz_recording_lookup_result()` function returns a `MusicbrainzRecordingLookupResult` object:

**Success Case:**

```python
result = MusicbrainzRecordingLookupResult(
    recording=MusicbrainzRecording(...),  # Recording object
    missing_cause=None                     # None on success
)

# Properties:
result.is_success  # True
result.recording   # MusicbrainzRecording instance
# result.missing_cause  # Raises ValueError (not available on success)
```

**Failure Case:**

```python
result = MusicbrainzRecordingLookupResult(
    recording=None,                        # None on failure
    missing_cause=MbRecordingMissingCause(...)  # Missing cause object
)

# Properties:
result.is_success      # False
# result.recording      # Raises ValueError (not available on failure)
result.missing_cause   # MbRecordingMissingCause instance
```

### MusicbrainzRecording Model

The `MusicbrainzRecording` model has the following fields:

```python
class MusicbrainzRecording:
    musicbrainz_id: str           # MusicBrainz recording UUID (primary key)
    title: str                    # Recording title
    score: Decimal                # Confidence score (0.0-1.0)
    duration_in_sec: int | None   # Duration in seconds (nullable)
    release_date: date | None     # Earliest release date (nullable)
    musicbrainz_link: str        # Auto-generated MusicBrainz URL (read-only)
    musicbrainz_artists: ManyToMany[MbArtist]  # Related artists
    
    # Computed properties:
    duration_str_in_hour_min_sec: str | None  # Formatted duration string
```

**Example:**

```python
recording = MusicbrainzRecording.objects.get(musicbrainz_id="...")
print(recording.musicbrainz_id)        # "4a45b00b-273d-40ed-9ecd-42f387f59c22"
print(recording.title)                  # "Drown (Massano remix)"
print(recording.score)                  # 0.95
print(recording.duration_in_sec)       # 440
print(recording.release_date)           # 2023-06-15 (or None)
print(recording.musicbrainz_link)       # "https://musicbrainz.org/recording/..."
print(recording.duration_str_in_hour_min_sec)  # "0:07:20"
```

### MbRecordingMissingCause Model

When a lookup fails, a `MbRecordingMissingCause` object is created:

```python
class MbRecordingMissingCause:
    user: User                      # User who attempted the lookup
    code: MbRecordingMissingCauseCode  # Error code (see Missing Cause Codes)
    message: str | None            # Error message (nullable, truncated if too long)
```

**Example:**

```python
missing_cause = result.missing_cause
print(missing_cause.code.code)     # "LOOKUP_FOUND_NO_MATCHING_RECORDING"
print(missing_cause.message)       # "No matching recordings found" (or None)
```

## Error Handling

The MusicBrainz integration includes custom exception classes for handling different types of errors:

- `InvalidFingerprintMusicbrainzRecordingLookupException`: Raised when the fingerprint is invalid (AcoustID error code 3)
- `InternalErrorMusicbrainzRecordingLookupException`: Raised when AcoustID has an internal error (error code 5)
- `DNSResolutionErrorMusicbrainzRecordingLookupException`: Raised when there's a DNS resolution error connecting to AcoustID
- `UnknownErrorCodeMusicbrainzRecordingLookupException`: Raised for unknown AcoustID error codes
- `UnknownStatusMusicbrainzRecordingLookupException`: Raised when the API returns an unknown status

Example error handling:

```python
from bodzify_api.exception import musicbrainz as musicbrainz_exception
from bodzify_api.utils.musicbrainz.service import get_musicbrainz_recording_lookup_result

try:
    result = get_musicbrainz_recording_lookup_result(user, fingerprint, duration_in_sec)
    if result.is_success:
        # Process recording
        pass
    else:
        # Handle missing cause
        print(f"Lookup failed: {result.missing_cause.code.code}")
except musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException:
    # Handle invalid fingerprint
    pass
except musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException:
    # Handle network error
    pass
except musicbrainz_exception.MusicbrainzRecordingLookupException as e:
    # Handle other MusicBrainz errors
    pass
```

### Missing Cause Codes

When a lookup fails, the system stores a `MbRecordingMissingCause` with one of these codes:

- `DURATION_BELOW_OR_EQUAL_1_SEC`: Track duration is too short (≤ 1 second)
- `LOOKUP_FOUND_NO_MATCHING_RECORDING`: No matching recordings found in AcoustID
- `LOOKUP_FAILED_DUE_TO_INVALID_FINGERPRINT`: Invalid fingerprint format
- `LOOKUP_FAILED_WITH_INTERNAL_ERROR`: AcoustID internal error
- `LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE`: Unknown error code from AcoustID
- `LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_STATUS_CODE`: Unknown status code from AcoustID
- `LOOKUP_FAILED_DNS_RESOLUTION_ERROR`: Network/DNS error

## Models

The MusicBrainz integration includes several models:

1. **`MusicbrainzRecording`**: Represents a recording from MusicBrainz
   - Fields: `musicbrainz_id`, `title`, `score`, `duration_in_sec`, `release_date`
   - Many-to-many relationship with `MbArtist`
   - Auto-generated `musicbrainz_link` field

2. **`MbArtist`**: Represents an artist from MusicBrainz
   - Fields: `musicbrainz_id`, `name`
   - Many-to-many relationship with recordings

3. **`MbRecordingMissingCause`**: Tracks why a lookup failed
   - Fields: `code`, `message`, `user`
   - One-to-one relationship with `TrackFile` when lookup fails

## Testing

Unit tests for the MusicBrainz integration are located in `bodzify_api/test/unit/utils/musicbrainz/`. These tests:

- Mock only the API response (AcoustID lookup)
- Use real database operations to test create/update logic
- Verify recording selection and metadata extraction

Example test structure:

```python
@pytest.mark.django_db
def test_create_new_recording_then_created():
    # recording_dict represents mocked API response
    recording_dict = {
        ApiFields.Names.TITLE: "Test Track",
        # ... other fields
    }
    recording = create_or_update_musicbrainz_recording_instance_from_dict(
        musicbrainz_id, recording_dict
    )
    # Assertions...
```

## References

- [AcoustID Web Service](https://acoustid.org/webservice)
- [MusicBrainz Database](https://musicbrainz.org/)
- [Chromaprint](https://acoustid.org/chromaprint)
