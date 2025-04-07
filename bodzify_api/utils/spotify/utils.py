from django.core.exceptions import ObjectDoesNotExist

from bodzify_api.model.spotify.children.artist.SpotifyArtist import SpotifyArtist
from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from .ApiFields import ApiFields


def batch_fetch_artist_details(artist_ids: list[str], user) -> dict[str, dict]:
    """
    Fetch details for multiple artists in batches of 50 (Spotify's limit).

    Args:
        artist_ids: List of Spotify artist IDs
        user: User instance to check Spotify authentication

    Returns:
        Dictionary mapping artist IDs to their full details
    """
    from .service import SpotifyAPIService
    service = SpotifyAPIService()
    artist_details = {}

    # Process in batches of 50 (Spotify's limit)
    batch_size = 50
    for i in range(0, len(artist_ids), batch_size):
        batch = artist_ids[i:i + batch_size]
        try:
            # Fetch all artists in the batch
            results = service.spotify.artists(batch)
            if results and 'artists' in results:
                for artist in results['artists']:
                    if artist:  # Skip any None results
                        artist_details[artist['id']] = artist
        except Exception as e:
            print(f"Error fetching artist batch: {str(e)}")
            # Continue with next batch even if one fails

    return artist_details


def create_spotify_artist_instance_from_dict(
        spotify_artist_id: str, spotify_artist_dict: dict, artist_details: dict | None = None) -> SpotifyArtist:
    """
    Create a SpotifyArtist instance from a Spotify API response dictionary.

    Args:
        spotify_artist_id: The Spotify ID of the artist
        spotify_artist_dict: The dictionary containing artist data from Spotify API
        artist_details: Optional dictionary of pre-fetched artist details

    Returns:
        A SpotifyArtist model instance
    """
    # Use pre-fetched details if available, otherwise use what we have
    if artist_details and spotify_artist_id in artist_details:
        spotify_artist_dict = artist_details[spotify_artist_id]

    name = spotify_artist_dict.get(ApiFields.Names.NAME, "Unknown Artist")
    popularity = spotify_artist_dict.get(ApiFields.Names.POPULARITY, 0)
    genres = spotify_artist_dict.get(ApiFields.Names.GENRES, [])
    images = spotify_artist_dict.get(ApiFields.Names.IMAGES, [])

    # Create or get the artist
    try:
        spotify_artist = SpotifyArtist.objects.get(spotify_id=spotify_artist_id)
        # Update existing artist if we have new data
        if genres or images:
            spotify_artist.genres = genres
            spotify_artist.images = images
            spotify_artist.save(update_fields=['genres', 'images'])
    except ObjectDoesNotExist:
        spotify_artist = SpotifyArtist.objects.create(
            spotify_id=spotify_artist_id,
            name=name,
            popularity=popularity,
            genres=genres,
            images=images
        )

    return spotify_artist


def create_spotify_lib_track_instance_from_dict(
        spotify_lib_track_id: str, spotify_lib_track_dict: dict, artist_details: dict | None = None) -> SpotifyLibTrack:
    """
    Create a SpotifyLibTrack instance from a Spotify API response dictionary.

    Args:
        spotify_lib_track_id: The Spotify ID of the track
        spotify_lib_track_dict: The dictionary containing track data from Spotify API
        artist_details: Optional dictionary of pre-fetched artist details

    Returns:
        A SpotifyLibTrack model instance
    """
    name = spotify_lib_track_dict.get(ApiFields.Names.NAME, "Unknown Track")
    duration_ms = spotify_lib_track_dict.get(ApiFields.Names.DURATION_MS, 0)
    popularity = spotify_lib_track_dict.get(ApiFields.Names.POPULARITY, 0)
    album = spotify_lib_track_dict.get(ApiFields.Names.ALBUM, {})
    preview_url = spotify_lib_track_dict.get(ApiFields.Names.PREVIEW_URL)
    explicit = spotify_lib_track_dict.get(ApiFields.Names.EXPLICIT, False)

    # Try to get existing track or create a new one
    try:
        spotify_lib_track = SpotifyLibTrack.objects.get(spotify_id=spotify_lib_track_id)
    except ObjectDoesNotExist:
        spotify_lib_track = SpotifyLibTrack.objects.create(
            spotify_id=spotify_lib_track_id,
            name=name,
            duration_ms=duration_ms,
            popularity=popularity,
            album=album,
            preview_url=preview_url,
            explicit=explicit
        )

    # Process artists
    artists_data = spotify_lib_track_dict.get(ApiFields.Names.ARTISTS, [])
    if artists_data:
        for artist_data in artists_data:
            artist_id = artist_data.get(ApiFields.Names.ID)
            if artist_id:
                artist = create_spotify_artist_instance_from_dict(artist_id, artist_data, artist_details)
                spotify_lib_track.spotify_artists.add(artist)

    return spotify_lib_track


def get_track_by_isrc(track_results, isrc):
    """
    Find a track with a specific ISRC code in track search results

    Args:
        track_results: Dictionary containing track search results from Spotify API
        isrc: The ISRC code to search for

    Returns:
        Track dictionary or None if not found
    """
    if ApiFields.Names.TRACKS in track_results and ApiFields.Names.ITEMS in track_results[ApiFields.Names.TRACKS]:
        for track in track_results[ApiFields.Names.TRACKS][ApiFields.Names.ITEMS]:
            # Check external IDs for ISRC if available
            external_ids = track.get('external_ids', {})
            if external_ids.get('isrc') == isrc:
                return track
    return None
