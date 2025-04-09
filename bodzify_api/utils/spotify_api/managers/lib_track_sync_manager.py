
from django.utils import timezone

from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.utils.spotify_api.SpotifyClient import spotify_client
from bodzify_api.utils.spotify_api import utils as spotify_api_utils


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

    if not user.spotify_access_token:
        return tracks

    # Track which Spotify tracks we've seen in this quick sync
    seen_track_ids = set()

    # Get the last sync time to optimize fetching
    last_sync_time = user.spotify_library_last_synced_at

    while True:
        try:
            saved_tracks = spotify_client.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)

            items = saved_tracks.get('items', [])
            total = saved_tracks.get('total', 0)

            if not items:
                break

            all_processed = True

            for item in items:
                track_data = item.get('track', {})
                if not track_data:
                    continue

                track_id = track_data.get('id')
                if not track_id:
                    continue

                # Check added_at timestamp if we're doing time-based sync
                added_at_str = item.get('added_at')
                added_at = None

                if added_at_str:
                    added_at = timezone.datetime.fromisoformat(added_at_str.replace('Z', '+00:00'))

                    # If we have a last sync time and this track was added before that, we can stop processing
                    if last_sync_time and added_at <= last_sync_time:
                        all_processed = False
                        break

                seen_track_ids.add(track_id)

                track = SpotifyLibTrack.objects.filter(spotify_id=track_id).first()

                if track:
                    # Update existing track
                    track.last_synced_at = now
                    track.is_removed = False  # Ensure it's marked as not removed
                    track.save(update_fields=['last_synced_at', 'is_removed'])
                else:
                    # Create new track
                    track = spotify_api_utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
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
                break

        except spotify_exception.SpotifyResourceNotFoundException as e:
            break
        except spotify_exception.SpotifyRateLimitException as e:
            break
        except spotify_exception.SpotifyException as e:
            break
        except Exception as e:
            break

    # Update user's last sync time if we processed any tracks
    if tracks and len(seen_track_ids) > 0:
        user.spotify_library_last_synced_at = now
        user.save(update_fields=['spotify_library_last_synced_at'])

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

    if not user.spotify_access_token:
        return tracks

    # Get all existing track IDs
    existing_tracks = set(SpotifyLibTrack.objects.values_list('spotify_id', flat=True))

    # Track which Spotify tracks we've seen
    seen_track_ids = set()

    while True:
        try:
            saved_tracks = spotify_client.get_user_saved_tracks(user.spotify_access_token, limit=limit, offset=offset)

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
                    track = spotify_api_utils.create_spotify_lib_track_instance_from_dict(track_id, track_data)
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
