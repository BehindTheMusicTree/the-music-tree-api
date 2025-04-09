# Spotify Integration for Bodzify API

This module provides integration with Spotify's Web API, allowing the application to search for tracks, retrieve track details, get artist information, and more.

## Setup

### 1. Install Dependencies

The Spotify integration requires the `spotipy` library. Make sure it's installed:

```
pip install -r requirements.txt
```

### 2. Create a Spotify Developer Application

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in with your Spotify account
2. Click "Create an App"
3. Fill in the application details:
   - App name: "Bodzify API" (or your preferred name)
   - App description: Brief description of your application
   - Website: Your website URL (can be localhost for development)
   - Redirect URI: For the client credentials flow used in this integration, you can use:
     - Development: `http://localhost:{port}/spotify/callback/`
     - Production: `https://your-domain.com/spotify/callback/`

> **Note about Redirect URIs**: 
> - This integration uses the client credentials flow which doesn't actually use the redirect URI, but Spotify requires 
>one to be set
> - If you later implement user authentication with Spotify, you'll need a proper callback endpoint to handle the OAuth flow
> - You can add multiple redirect URIs in the Spotify dashboard for different environments

4. After creating the app, you'll see your Client ID and you can click "Show Client Secret" to view your secret

### 3. Configure Spotify API Credentials

Set the following environment variables with your Spotify API credentials:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

These credentials are from the Spotify Developer application you created in the previous step.

### 3. Run Migrations

Ensure the Spotify models are migrated to your database:

```
python manage.py makemigrations
python manage.py migrate
```

## Testing the Integration

A management command is provided to test the Spotify API connection:

```
python manage.py spotify_connection_test
```

You can also test specific functionality:

```
# Test search functionality
python manage.py spotify_connection_test --search "your search query"

# Test getting a track by ID
python manage.py spotify_connection_test --track "spotify_lib_track_id"

# Test getting an artist by ID
python manage.py spotify_connection_test --artist "spotify_artist_id"

# Test looking up a track by ISRC
python manage.py spotify_connection_test --isrc "isrc_code"
```

## Usage

### Searching for tracks

```python
from bodzify_api.utils.spotify.service import search_spotify_lib_tracks

# Search for tracks
tracks = search_spotify_lib_tracks(user, "search query", limit=5)
for track in tracks:
    print(f"{track.name} - {track.spotify_artists.all()}")
```

### Getting a track by ID

```python
from bodzify_api.utils.spotify.service import get_or_create_spotify_lib_track

# Get a track by Spotify ID
track = get_or_create_spotify_lib_track(user, "spotify_lib_track_id")
if track:
    print(f"Track: {track.name}, Duration: {track.duration_str_in_hour_min_sec}")
```

### Using the Spotify API service directly

```python
from bodzify_api.utils.spotify.service import SpotifyAPIService

# Create a service instance
service = SpotifyAPIService()

# Get audio features for a track
features = service.get_audio_features("spotify_lib_track_id")
print(f"Tempo: {features.get('tempo')}, Key: {features.get('key')}")

# Get artist details
artist = service.get_artist_by_id("spotify_artist_id")
print(f"Artist: {artist.get('name')}, Popularity: {artist.get('popularity')}")
```

## Error Handling

The Spotify integration includes custom exception classes for handling different types of errors:

- `SpotifyAuthenticationException`: Raised when authentication with Spotify fails
- `SpotifyResourceNotFoundException`: Raised when a requested resource is not found
- `SpotifyRateLimitException`: Raised when Spotify API rate limit is exceeded
- `SpotifyNetworkException`: Raised when there's a network error
- `SpotifyAPIException`: Raised for general Spotify API errors

Example error handling:

```python
from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.utils.spotify.service import SpotifyAPIService

try:
    service = SpotifyAPIService()
    track = service.retrieve_track_by_id("spotify_lib_track_id")
    # Process track data
except spotify_exception.SpotifyResourceNotFoundException:
    # Handle resource not found
except spotify_exception.SpotifyAuthenticationException:
    # Handle authentication error
except spotify_exception.SpotifyException as e:
    # Handle other Spotify errors
```

## Models

The Spotify integration includes two main models:

1. `SpotifyArtist`: Represents an artist from Spotify
2. `SpotifyLibTrack`: Represents a track from Spotify with a many-to-many relationship to artists