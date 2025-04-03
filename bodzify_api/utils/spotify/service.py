import logging
from typing import Optional, Dict, List, Any

import spotipy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException as SpotipyException

from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.model.spotify_resource.children.track.SpotifyTrack import SpotifyTrack
from bodzify_api.model.user.User import User
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
            return self.spotify.search(q=query, type='track', limit=limit)
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
            return self.spotify.track(track_id)
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
            return self.spotify.artist(artist_id)
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
            return self.spotify.audio_features(track_id)[0]
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


def get_or_create_spotify_track(user: User, track_id: str) -> Optional[SpotifyTrack]:
    """
    Get or create a SpotifyTrack instance for the given Spotify track ID

    Args:
        user: User making the request
        track_id: Spotify track ID

    Returns:
        SpotifyTrack instance or None if track not found
    """
    try:
        # Check if the track already exists in our database
        try:
            return SpotifyTrack.objects.get(spotify_id=track_id)
        except ObjectDoesNotExist:
            # Track doesn't exist, fetch from Spotify API
            service = SpotifyAPIService()
            try:
                track_data = service.get_track_by_id(track_id)
                if track_data:
                    return utils.create_spotify_track_instance_from_dict(track_id, track_data)
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


def search_spotify_tracks(user: User, query: str, limit: int = 5) -> List[SpotifyTrack]:
    """
    Search for tracks on Spotify and create track models for the results

    Args:
        user: User making the request
        query: Search query
        limit: Maximum number of results

    Returns:
        List of SpotifyTrack instances
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
                        track = utils.create_spotify_track_instance_from_dict(track_id, track_data)
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
