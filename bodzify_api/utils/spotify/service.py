import logging
from typing import Optional, Dict, List, Any
from django.utils import timezone
import time

import spotipy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException as SpotipyException

from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from . import utils
from .ApiFields import ApiFields

logger = logging.getLogger(settings.APP_NAME)


class SpotifyAPIService:
    """Service class for interacting with the Spotify API"""

    def __init__(self):
        """Initialize with Spotify API credentials from settings"""
        try:
            credentials_manager = SpotifyClientCredentials(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET
            )
            self.spotify = spotipy.Spotify(client_credentials_manager=credentials_manager)
        except SpotipyException as e:
            logger.error(f"Spotify authentication error: {str(e)}")
            raise spotify_exception.SpotifyAuthenticationException(f"Failed to authenticate with Spotify: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during Spotify client initialization: {str(e)}")
            raise spotify_exception.SpotifyAPIException(f"Unexpected error: {str(e)}")

    def search_track(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search for tracks on Spotify

        Args:
            query: The search query
            limit: Maximum number of results to return (default: 5)

        Returns:
            Dictionary containing search results
        """
        try:
            result = self.spotify.search(q=query, type='track', limit=limit)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify search error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException(f"No results found for query: {query}")
            elif "rate limit" in str(e).lower():
                raise spotify_exception.SpotifyRateLimitException("Spotify API rate limit exceeded")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error during Spotify search: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_track_by_id(self, track_id: str) -> Dict[str, Any]:
        """
        Get track details by Spotify track ID

        Args:
            track_id: Spotify track ID

        Returns:
            Dictionary containing track details
        """
        try:
            result = self.spotify.track(track_id)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify track fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException(f"Track not found: {track_id}")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching track: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_artist_by_id(self, artist_id: str) -> Dict[str, Any]:
        """
        Get artist details by Spotify artist ID

        Args:
            artist_id: Spotify artist ID

        Returns:
            Dictionary containing artist details
        """
        try:
            result = self.spotify.artist(artist_id)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify artist fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException(f"Artist not found: {artist_id}")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching artist: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_track_by_isrc(self, isrc: str) -> Optional[Dict[str, Any]]:
        """
        Find a track by its ISRC code

        Args:
            isrc: The ISRC code

        Returns:
            Track details dictionary or None if not found
        """
        try:
            # Search using the ISRC directly
            results = self.spotify.search(q=f"isrc:{isrc}", type='track')
            return utils.get_track_by_isrc(results, isrc)
        except SpotipyException as e:
            logger.error(f"Spotify ISRC lookup error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Network error during ISRC lookup: {str(e)}")
            return None

    def get_audio_features(self, track_id: str) -> Dict[str, Any]:
        """
        Get audio features for a track

        Args:
            track_id: Spotify track ID

        Returns:
            Dictionary containing audio features
        """
        try:
            features = self.spotify.audio_features(track_id)
            if features is None or len(features) == 0:
                return {}
            return features[0]
        except SpotipyException as e:
            logger.error(f"Spotify audio features error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException(
                    f"Audio features not found for track: {track_id} ")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching audio features: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_user_saved_tracks(self, access_token: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get tracks saved in the user's Spotify library

        Args:
            access_token: User's Spotify access token
            limit: Maximum number of tracks to return (default: 50)
            offset: Offset for pagination (default: 0)

        Returns:
            Dictionary containing saved tracks
        """
        try:
            sp = spotipy.Spotify(auth=access_token)
            result = sp.current_user_saved_tracks(limit=limit, offset=offset)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify saved tracks fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException("User's saved tracks not found")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching saved tracks: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_user_playlists(self, access_token: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get user's playlists

        Args:
            access_token: User's Spotify access token
            limit: Maximum number of playlists to return (default: 50)
            offset: Offset for pagination (default: 0)

        Returns:
            Dictionary containing user's playlists
        """
        try:
            sp = spotipy.Spotify(auth=access_token)
            result = sp.current_user_playlists(limit=limit, offset=offset)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify playlists fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException("User's playlists not found")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching playlists: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_user_saved_albums(self, access_token: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get user's saved albums

        Args:
            access_token: User's Spotify access token
            limit: Maximum number of albums to return (default: 50)
            offset: Offset for pagination (default: 0)

        Returns:
            Dictionary containing user's saved albums
        """
        try:
            sp = spotipy.Spotify(auth=access_token)
            result = sp.current_user_saved_albums(limit=limit, offset=offset)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify saved albums fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException("User's saved albums not found")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching saved albums: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def get_user_followed_artists(self, access_token: str, limit: int = 50, after: str | None = None) -> Dict[str, Any]:
        """
        Get user's followed artists

        Args:
            access_token: User's Spotify access token
            limit: Maximum number of artists to return (default: 50)
            after: Cursor for pagination (default: None)

        Returns:
            Dictionary containing user's followed artists
        """
        try:
            sp = spotipy.Spotify(auth=access_token)
            result = sp.current_user_followed_artists(limit=limit, after=after)
            if result is None:
                return {}
            return result
        except SpotipyException as e:
            logger.error(f"Spotify followed artists fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException("User's followed artists not found")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching followed artists: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def _get_authenticated_client(self, access_token: str) -> spotipy.Spotify:
        """
        Get a Spotify client authenticated with user's access token.

        Args:
            access_token: User's Spotify access token

        Returns:
            Authenticated Spotify client
        """
        if not access_token:
            raise spotify_exception.SpotifyAuthenticationException("No access token provided")
        return spotipy.Spotify(auth=access_token)

    def get_artists(self, artist_ids: list[str], access_token: str) -> dict[str, dict]:
        """
        Get details for multiple artists in a single API call.

        Args:
            artist_ids: List of Spotify artist IDs (max 50)
            access_token: User's Spotify access token

        Returns:
            Dictionary mapping artist IDs to their details
        """
        try:
            sp = self._get_authenticated_client(access_token)
            results = sp.artists(artist_ids)
            if results is None or 'artists' not in results:
                return {}

            artist_details = {}
            for artist in results['artists']:
                if artist:  # Skip any None results
                    artist_details[artist['id']] = artist
            return artist_details
        except SpotipyException as e:
            logger.error(f"Spotify artists batch fetch error: {str(e)}")
            if "not found" in str(e).lower():
                raise spotify_exception.SpotifyResourceNotFoundException(f"Artists not found: {artist_ids}")
            else:
                raise spotify_exception.SpotifyAPIException(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Network error fetching artists: {str(e)}")
            raise spotify_exception.SpotifyNetworkException(f"Network error: {str(e)}")

    def quick_sync_library(self, user: SpotifyUser) -> list[SpotifyLibTrack]:
        if not user.spotify_access_token:
            return []

        tracks = []
        offset = 0
        limit = 50
        last_sync_time = user.spotify_library_last_synced_at

        while True:
            try:
                items, total = self._fetch_tracks_batch(user, offset, limit)
                if not items:
                    break

                for track_data in items:
                    if not track_data:
                        continue

                    track_id = track_data.get('id')
                    if not track_id:
                        continue

                    track = self._process_track(user, track_data, last_sync_time)
                    if track:
                        tracks.append(track)

                offset += limit
                if offset >= total:
                    break

            except Exception as e:
                if isinstance(e, spotify_exception.SpotifyAPIError):
                    if e.status_code == 404:
                        break
                    elif e.status_code == 429:
                        time.sleep(1)
                        continue
                raise

        user.spotify_library_last_synced_at = timezone.now()
        user.save()

        return tracks

    def sync_library(self, user: SpotifyUser) -> list[SpotifyLibTrack]:
        if not user.spotify_access_token:
            return []

        tracks = []
        offset = 0
        limit = 50
        existing_tracks = set(SpotifyLibTrack.objects.values_list('spotify_id', flat=True))
        existing_track_ids = set(existing_tracks)

        while True:
            try:
                items, total = self._fetch_tracks_batch(user, offset, limit)
                if not items:
                    break

                for track_data in items:
                    if not track_data or not track_data.get('id'):
                        continue

                    track_id = track_data['id']
                    track = self._process_track(user, track_data)
                    if track:
                        tracks.append(track)
                        if track_id in existing_track_ids:
                            existing_track_ids.remove(track_id)

                offset += limit
                if offset >= total:
                    break

            except Exception as e:
                if isinstance(e, spotify_exception.SpotifyAPIError):
                    if e.status_code == 404:
                        break
                    elif e.status_code == 429:
                        time.sleep(1)
                        continue
                raise

        removed_tracks = existing_track_ids - set(track.spotify_id for track in tracks)
        if removed_tracks:
            SpotifyLibTrack.objects.filter(spotify_id__in=removed_tracks).update(is_removed=True)
            for track_id in removed_tracks:
                print(f"Track marked as removed: {track_id}")

        user.spotify_library_last_synced_at = timezone.now()
        user.save()

        return tracks


def get_or_create_spotify_lib_track(user: SpotifyUser, track_id: str) -> Optional[SpotifyLibTrack]:
    """
    Get or create a SpotifyLibTrack instance for the given Spotify track ID

    Args:
        user: User making the request
        track_id: Spotify track ID

    Returns:
        SpotifyLibTrack instance or None if track not found
    """
    try:
        # Check if the track already exists in our database
        try:
            return SpotifyLibTrack.objects.get(spotify_id=track_id)
        except ObjectDoesNotExist:
            # Track doesn't exist, fetch from Spotify API
            service = SpotifyAPIService()
            try:
                track_data = service.get_track_by_id(track_id)
                if track_data:
                    return utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
                return None
            except spotify_exception.SpotifyResourceNotFoundException:
                logger.info(f"Track not found on Spotify: {track_id}")
                return None
            except spotify_exception.SpotifyException as e:
                logger.error(f"Spotify API error: {str(e)}")
                return None

    except Exception as e:
        logger.error(f"Unexpected error getting Spotify track: {str(e)}")
        return None


def search_spotify_lib_tracks(user: SpotifyUser, query: str, limit: int = 5) -> List[SpotifyLibTrack]:
    """
    Search for tracks on Spotify and create track models for the results

    Args:
        user: User making the request
        query: Search query
        limit: Maximum number of results

    Returns:
        List of SpotifyLibTrack instances
    """
    tracks = []
    try:
        service = SpotifyAPIService()
        try:
            results = service.search_track(query, limit)

            if ApiFields.Names.TRACKS in results and ApiFields.Names.ITEMS in results[ApiFields.Names.TRACKS]:
                for track_data in results[ApiFields.Names.TRACKS][ApiFields.Names.ITEMS]:
                    track_id = track_data.get(ApiFields.Names.ID)
                    if track_id:
                        track = utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
                        tracks.append(track)
        except spotify_exception.SpotifyResourceNotFoundException:
            logger.info(f"No tracks found for query: {query}")
        except spotify_exception.SpotifyRateLimitException as e:
            logger.warning(f"Spotify rate limit exceeded: {str(e)}")
        except spotify_exception.SpotifyException as e:
            logger.error(f"Spotify API error during search: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error searching Spotify tracks: {str(e)}")

    return tracks


def quick_sync_spotify_library(user: SpotifyUser) -> list[SpotifyLibTrack]:
    """
    Perform a quick sync of a user's Spotify library, focusing on new additions only.
    This is designed to be faster for routine use and is automatically called when a user connects.

    Args:
        user: The user whose library should be synced

    Returns:
        list[SpotifyLibTrack]: List of newly synced track instances
    """
    tracks = []
    offset = 0
    limit = 50
    now = timezone.now()

    print(f"\n=== Starting Quick Spotify Library Sync for user {user.username} ===")
    print(f"Access token present: {bool(user.spotify_access_token)}")

    if not user.spotify_access_token:
        print("No access token available, cannot sync")
        return tracks

    service = SpotifyAPIService()

    # Track which Spotify tracks we've seen in this quick sync
    seen_track_ids = set()

    # Get the last sync time to optimize fetching
    last_sync_time = user.spotify_library_last_synced_at

    print(f"Last library sync at: {last_sync_time}")

    while True:
        try:
            print(f"\nFetching tracks with offset {offset} and limit {limit}")
            saved_tracks = service.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)

            items = saved_tracks.get('items', [])
            total = saved_tracks.get('total', 0)

            print(f"Total tracks in library: {total}")
            print(f"Items in current batch: {len(items)}")

            if not items:
                print("No more tracks to fetch")
                break

            print(f"\nProcessing {len(items)} tracks")
            all_processed = True

            for item in items:
                track_data = item.get('track', {})
                if not track_data:
                    print("Skipping empty track data")
                    continue

                track_id = track_data.get('id')
                if not track_id:
                    print("Skipping track with no ID")
                    continue

                # Check added_at timestamp if we're doing time-based sync
                added_at_str = item.get('added_at')
                added_at = None

                if added_at_str:
                    added_at = timezone.datetime.fromisoformat(added_at_str.replace('Z', '+00:00'))

                    # If we have a last sync time and this track was added before that, we can stop processing
                    if last_sync_time and added_at <= last_sync_time:
                        print(
                            f"Track added at {added_at} is older than last sync at {last_sync_time}, skipping further tracks")
                        all_processed = False
                        break

                seen_track_ids.add(track_id)
                print(f"\nProcessing new track: {track_data.get('name', 'Unknown')}")
                print(f"Track ID: {track_id}")

                track = SpotifyLibTrack.objects.filter(spotify_id=track_id).first()

                if track:
                    # Update existing track
                    track.last_synced_at = now
                    track.is_removed = False  # Ensure it's marked as not removed
                    track.save(update_fields=['last_synced_at', 'is_removed'])
                    print(f"Marked existing track as not removed: {track.name}")
                else:
                    # Create new track
                    track = utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
                    if track:
                        track.last_synced_at = now
                        track.save()
                        print(f"Created new track: {track.name}")

                if track:
                    tracks.append(track)

            # If we finished processing all tracks in this batch and didn't break early due to old tracks
            if all_processed:
                offset += limit
                print(f"\nCurrent offset: {offset}, Total processed: {len(tracks)}")
            else:
                # We found older tracks, no need to fetch more
                break

        except spotify_exception.SpotifyResourceNotFoundException as e:
            print(f"Resource not found: {str(e)}")
            break
        except spotify_exception.SpotifyRateLimitException as e:
            print(f"Rate limit hit: {str(e)}")
            break
        except spotify_exception.SpotifyException as e:
            print(f"Spotify API error: {str(e)}")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            break

    # Update user's last sync time if we processed any tracks
    if tracks and len(seen_track_ids) > 0:
        user.spotify_library_last_synced_at = now
        user.save(update_fields=['spotify_library_last_synced_at'])
        print(f"Updated user's last sync time to {now}")

    print(f"\n=== Quick Sync Complete ===")
    print(f"Total new tracks synced: {len(tracks)}")
    if tracks:
        print("\nFirst few new tracks:")
        for track in tracks[:5]:
            print(f"- {track.name} by {', '.join(artist.name for artist in track.spotify_artists.all())}")
    return tracks


def full_sync_spotify_library(user: SpotifyUser) -> list[SpotifyLibTrack]:
    """
    Perform a complete sync of a user's Spotify library by fetching all saved tracks.
    This handles both new additions and removals, but is more resource-intensive than quick_sync.

    Args:
        user: The user whose library should be synced

    Returns:
        list[SpotifyLibTrack]: List of synced track instances
    """
    tracks = []
    offset = 0
    limit = 50
    now = timezone.now()

    print(f"\n=== Starting Spotify Library Sync for user {user.username} ===")
    print(f"Access token present: {bool(user.spotify_access_token)}")
    print(f"Performing FULL SYNC (checks additions and removals)")

    if not user.spotify_access_token:
        print("No access token available, cannot sync")
        return tracks

    service = SpotifyAPIService()

    # Get all existing track IDs
    existing_tracks = set(SpotifyLibTrack.objects.values_list('spotify_id', flat=True))

    print(f"Found {len(existing_tracks)} existing tracks")

    # Track which Spotify tracks we've seen
    seen_track_ids = set()

    while True:
        try:
            print(f"\nFetching tracks with offset {offset} and limit {limit}")
            saved_tracks = service.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)

            items = saved_tracks.get('items', [])
            total = saved_tracks.get('total', 0)

            print(f"Total tracks in library: {total}")
            print(f"Items in current batch: {len(items)}")

            if not items:
                print("No more tracks to fetch")
                break

            print(f"\nProcessing {len(items)} tracks")
            for item in items:
                track_data = item.get('track', {})
                if not track_data:
                    print("Skipping empty track data")
                    continue

                track_id = track_data.get('id')
                if not track_id:
                    print("Skipping track with no ID")
                    continue

                seen_track_ids.add(track_id)
                print(f"\nProcessing track: {track_data.get('name', 'Unknown')}")
                print(f"Track ID: {track_id}")

                # Check if track exists and needs update
                track = SpotifyLibTrack.objects.filter(spotify_id=track_id).first()
                needs_update = True

                if track:
                    # Only update if track data has changed
                    if (track.name != track_data.get('name') or
                        track.popularity != track_data.get('popularity') or
                            track.duration_ms != track_data.get('duration_ms')):
                        print("Track data has changed, updating...")
                    else:
                        print("Track unchanged, skipping update")
                        needs_update = False
                        track.last_synced_at = now
                        track.is_removed = False  # Mark as not removed
                        track.save()
                        tracks.append(track)
                        continue

                if needs_update:
                    track = utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
                    if track:
                        track.last_synced_at = now
                        track.is_removed = False  # Mark as not removed
                        track.save()
                        print(f"Successfully created/updated track: {track.name}")
                        print(f"Artists: {', '.join(artist.name for artist in track.spotify_artists.all())}")
                        tracks.append(track)
                    else:
                        print("Failed to create/update track")

            offset += limit
            print(f"\nCurrent offset: {offset}, Total processed: {len(tracks)}")

        except spotify_exception.SpotifyResourceNotFoundException as e:
            print(f"Resource not found: {str(e)}")
            break
        except spotify_exception.SpotifyRateLimitException as e:
            print(f"Rate limit hit: {str(e)}")
            break
        except spotify_exception.SpotifyException as e:
            print(f"Spotify API error: {str(e)}")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            break

    # Find tracks that were removed from Spotify library
    removed_tracks = existing_tracks - seen_track_ids
    if removed_tracks:
        print(f"\nFound {len(removed_tracks)} tracks that were removed from Spotify library")
        # Mark these tracks as removed
        SpotifyLibTrack.objects.filter(spotify_id__in=removed_tracks).update(is_removed=True)
        for track_id in removed_tracks:
            print(f"Track marked as removed: {track_id}")

    # Update user's last sync time
    user.spotify_library_last_synced_at = now
    user.save(update_fields=['spotify_library_last_synced_at'])
    print(f"Updated user's last sync time to {now}")

    print(f"\n=== Full Sync Complete ===")
    print(f"Total tracks synced: {len(tracks)}")
    if tracks:
        print("\nFirst few tracks:")
        for track in tracks[:5]:
            print(f"- {track.name} by {', '.join(artist.name for artist in track.spotify_artists.all())}")
    return tracks
