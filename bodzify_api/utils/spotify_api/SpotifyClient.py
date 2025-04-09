import logging
from typing import Optional, Dict, Any

import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException as SpotipyException

from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from . import utils

logger = logging.getLogger(settings.APP_NAME)


class SpotifyClient:

    def __init__(self):
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

    def retrieve_track_by_id(self, track_id: str) -> Dict[str, Any]:
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

    def retrieve_track_by_isrc(self, isrc: str) -> Optional[Dict[str, Any]]:
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
            return utils.retrieve_track_by_isrc_from_track_results(results, isrc)
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

    def _fetch_tracks_batch(self, user: SpotifyUser, offset: int, limit: int) -> tuple[list[dict], int]:
        if not user.spotify_access_token:
            return [], 0
        saved_tracks = self.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)
        items = saved_tracks.get('items', [])
        total = saved_tracks.get('total', 0)
        return [item['track'] for item in items if item.get('track')], total
