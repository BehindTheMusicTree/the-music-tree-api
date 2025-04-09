import logging
from typing import Optional, List
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.exception import spotify as spotify_exception
from .SpotifyClient import SpotifyClient
from . import utils
from .ApiFields import ApiFields

logger = logging.getLogger(__name__)


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
            client = SpotifyClient()
            try:
                track_data = client.retrieve_track_by_id(track_id)
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
        client = SpotifyClient()
        try:
            results = client.search_track(query, limit)

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


def quick_sync_spotify_lib_tracks(user: SpotifyUser) -> list[SpotifyLibTrack]:
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

    client = SpotifyClient()

    # Track which Spotify tracks we've seen in this quick sync
    seen_track_ids = set()

    # Get the last sync time to optimize fetching
    last_sync_time = user.spotify_library_last_synced_at

    print(f"Last library sync at: {last_sync_time}")

    while True:
        try:
            print(f"\nFetching tracks with offset {offset} and limit {limit}")
            saved_tracks = client.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)

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


def full_sync_spotify_lib_tracks(user: SpotifyUser) -> list[SpotifyLibTrack]:
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

    client = SpotifyClient()

    # Get all existing track IDs
    existing_tracks = set(SpotifyLibTrack.objects.values_list('spotify_id', flat=True))

    print(f"Found {len(existing_tracks)} existing tracks")

    # Track which Spotify tracks we've seen
    seen_track_ids = set()

    while True:
        try:
            print(f"\nFetching tracks with offset {offset} and limit {limit}")
            saved_tracks = client.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)

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
