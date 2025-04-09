import logging
from typing import Optional, List

from django.core.exceptions import ObjectDoesNotExist

from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.exception import spotify as spotify_exception
from ..SpotifyClient import SpotifyClient
from .. import utils
from ..ApiFields import ApiFields

logger = logging.getLogger(__name__)

spotify_client = SpotifyClient()


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
            try:
                track_data = spotify_client.retrieve_track_by_id(track_id)
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
        try:
            results = spotify_client.search_track(query, limit)

            if results and ApiFields.Names.TRACKS in results and ApiFields.Names.ITEMS in results[ApiFields.Names.TRACKS]:
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


def retrieve_track_by_isrc(isrc: str) -> Optional[SpotifyLibTrack]:
    """
    Retrieve a SpotifyLibTrack instance by ISRC code

    Args:
        isrc: ISRC code

    Returns:
        SpotifyLibTrack instance or None if track not found
    """
    try:
        results = spotify_client.search_track(f"isrc:{isrc}", limit=1)
        if results and ApiFields.Names.TRACKS in results and ApiFields.Names.ITEMS in results[ApiFields.Names.TRACKS]:
            for track_data in results[ApiFields.Names.TRACKS][ApiFields.Names.ITEMS]:
                track_id = track_data.get(ApiFields.Names.ID)
                if track_id:
                    return utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
    except Exception as e:
        logger.error(f"Unexpected error retrieving track by ISRC: {str(e)}")
