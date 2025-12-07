import logging
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.model.user.spotify.SpotifyUser import SpotifyUser
from api.exception import spotify as spotify_exception
from ..SpotifyClient import SpotifyClient
from ..ApiFields import ApiFields
from .. import utils

logger = logging.getLogger(__name__)


class SpotifyApiLibTrackManager:
    def __init__(self):
        self.spotify_client = SpotifyClient()

    def get_or_create_spotify_lib_track(self, user: SpotifyUser, track_id: str) -> SpotifyLibTrack | None:
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
                    track_data = self.spotify_client.retrieve_track_by_id(track_id)
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

    def search_spotify_lib_tracks(self, user: SpotifyUser, query: str, limit: int = 5) -> List[SpotifyLibTrack]:
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
                results = self.spotify_client.search_track(query, limit)

                if results and ApiFields.Names.TRACKS in results and ApiFields.Names.ITEMS in results[
                        ApiFields.Names.TRACKS]:
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

    def retrieve_track_by_isrc(self, isrc: str) -> Optional[SpotifyLibTrack]:
        """
        Retrieve a SpotifyLibTrack instance by ISRC code

        Args:
            isrc: ISRC code

        Returns:
            SpotifyLibTrack instance or None if track not found
        """
        try:
            results = self.spotify_client.search_track(f"isrc:{isrc}", limit=1)
            if results and ApiFields.Names.TRACKS in results and ApiFields.Names.ITEMS in results[ApiFields.Names.TRACKS]:
                for track_data in results[ApiFields.Names.TRACKS][ApiFields.Names.ITEMS]:
                    track_id = track_data.get(ApiFields.Names.ID)
                    if track_id:
                        return utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
        except Exception as e:
            logger.error(f"Unexpected error retrieving track by ISRC: {str(e)}")

    def quick_sync(self, user: SpotifyUser) -> list[SpotifyLibTrack]:
        """
        Perform a quick sync of a user's Spotify library, focusing on new additions only.
        This is designed to be faster for routine use and is automatically called when a user connects.

        Args:
            user: The user whose library should be synced

        Returns:
            list[SpotifyLibTrack]: List of newly synced track instances
        """
        logger.info(f"Starting quick sync for user {user.spotify_id}")
        tracks = []
        offset = 0
        limit = 50
        now = timezone.now()

        if not user.spotify_access_token:
            logger.warning(f"No access token found for user {user.spotify_id}")
            return tracks

        # Track which Spotify tracks we've seen in this quick sync
        seen_track_ids = set()

        # Get the last sync time to optimize fetching
        last_sync_time = user.spotify_library_last_synced_at
        logger.info(f"Last sync time: {last_sync_time}")

        while True:
            try:
                logger.debug(f"Fetching saved tracks batch - offset: {offset}, limit: {limit}")
                saved_tracks = self.spotify_client.get_user_saved_tracks(
                    user.spotify_access_token, limit=limit, offset=offset)

                items = saved_tracks.get('items', [])
                total = saved_tracks.get('total', 0)
                logger.debug(f"Retrieved {len(items)} tracks out of {total} total")

                if not items:
                    logger.info("No more tracks to process")
                    break

                all_processed = True

                for item in items:
                    track_data = item.get('track', {})
                    if not track_data:
                        logger.warning("Skipping item with no track data")
                        continue

                    track_id = track_data.get('id')
                    if not track_id:
                        logger.warning("Skipping track with no ID")
                        continue

                    # Check added_at timestamp if we're doing time-based sync
                    added_at_str = item.get('added_at')
                    added_at = None

                    if added_at_str:
                        added_at = timezone.datetime.fromisoformat(added_at_str.replace('Z', '+00:00'))

                        # If we have a last sync time and this track was added before that, we can stop processing
                        if last_sync_time and added_at <= last_sync_time:
                            logger.info(f"Reached tracks older than last sync time ({last_sync_time})")
                            all_processed = False
                            break

                    seen_track_ids.add(track_id)

                    track = SpotifyLibTrack.objects.filter(spotify_id=track_id).first()

                    if track:
                        # Update existing track
                        logger.debug(f"Updating existing track {track_id}")
                        track.last_synced_at = now
                        track.is_removed = False  # Ensure it's marked as not removed
                        track.save(update_fields=['last_synced_at', 'is_removed'])
                    else:
                        # Create new track
                        logger.info(f"Creating new track {track_id}")
                        track = utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
                        if track:
                            track.last_synced_at = now
                            track.save()

                    if track:
                        tracks.append(track)

                # If we finished processing all tracks in this batch and didn't break early due to old tracks
                if all_processed:
                    offset += limit
                else:
                    # We found older tracks, no need to fetch more
                    logger.info("Stopping sync as we reached older tracks")
                    break

            except spotify_exception.SpotifyResourceNotFoundException as e:
                logger.error(f"Resource not found: {str(e)}")
                break
            except spotify_exception.SpotifyRateLimitException as e:
                logger.warning(f"Rate limit exceeded: {str(e)}")
                break
            except spotify_exception.SpotifyException as e:
                logger.error(f"Spotify API error: {str(e)}")
                break
            except Exception as e:
                logger.error(f"Unexpected error during sync: {str(e)}")
                break

        # Update user's last sync time if we processed any tracks
        if tracks and len(seen_track_ids) > 0:
            logger.info(f"Updating last sync time for user {user.spotify_id} - processed {len(tracks)} tracks")
            user.spotify_library_last_synced_at = now
            user.save(update_fields=['spotify_library_last_synced_at'])
        else:
            logger.info("No tracks processed, skipping last sync time update")

        return tracks

    def full_sync(self, user: SpotifyUser) -> list[SpotifyLibTrack]:
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

        if not user.spotify_access_token:
            return tracks

        # Get all existing track IDs
        existing_tracks = set(SpotifyLibTrack.objects.values_list('spotify_id', flat=True))

        # Track which Spotify tracks we've seen
        seen_track_ids = set()

        while True:
            try:
                saved_tracks = self.spotify_client.get_user_saved_tracks(
                    user.spotify_access_token, limit=limit, offset=offset)

                items = saved_tracks.get('items', [])
                total = saved_tracks.get('total', 0)

                if not items:
                    break

                for item in items:
                    track_data = item.get('track', {})
                    if not track_data:
                        continue

                    track_id = track_data.get('id')
                    if not track_id:
                        continue

                    seen_track_ids.add(track_id)

                    # Check if track exists and needs update
                    track = SpotifyLibTrack.objects.filter(spotify_id=track_id).first()
                    needs_update = True

                    if track:
                        # Only update if track data has changed
                        if (track.name != track_data.get('name') or
                            track.popularity != track_data.get('popularity') or
                                track.duration_ms != track_data.get('duration_ms')):
                            pass
                        else:
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
                            tracks.append(track)

                offset += limit

            except spotify_exception.SpotifyResourceNotFoundException as e:
                break
            except spotify_exception.SpotifyRateLimitException as e:
                break
            except spotify_exception.SpotifyException as e:
                break
            except Exception as e:
                break

        # Find tracks that were removed from Spotify library
        removed_tracks = existing_tracks - seen_track_ids
        if removed_tracks:
            # Mark these tracks as removed
            SpotifyLibTrack.objects.filter(spotify_id__in=removed_tracks).update(is_removed=True)

        # Update user's last sync time
        user.spotify_library_last_synced_at = now
        user.save(update_fields=['spotify_library_last_synced_at'])

        return tracks
