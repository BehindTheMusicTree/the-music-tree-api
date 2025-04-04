from django.core.exceptions import ObjectDoesNotExist

from bodzify_api.model.spotify.children.artist.SpotifyArtist import SpotifyArtist
from bodzify_api.model.spotify.children.track.SpotifyTrack import SpotifyTrack
from .ApiFields import ApiFields


def create_spotify_artist_instance_from_dict(spotify_artist_id: str, spotify_artist_dict: dict) -> SpotifyArtist:
    """
    Create a SpotifyArtist instance from a Spotify API response dictionary.

    Args:
        spotify_artist_id: The Spotify ID of the artist
        spotify_artist_dict: The dictionary containing artist data from Spotify API

    Returns:
        A SpotifyArtist model instance
    """
    name = spotify_artist_dict.get(ApiFields.Names.NAME, "Unknown Artist")
    popularity = spotify_artist_dict.get(ApiFields.Names.POPULARITY, 0)
    genres = spotify_artist_dict.get(ApiFields.Names.GENRES, [])
    images = spotify_artist_dict.get(ApiFields.Names.IMAGES, [])

    # Create or get the artist
    try:
        spotify_artist = SpotifyArtist.objects.get(spotify_id=spotify_artist_id)
    except ObjectDoesNotExist:
        spotify_artist = SpotifyArtist.objects.create(
            spotify_id=spotify_artist_id,
            name=name,
            popularity=popularity,
            genres=genres,
            images=images
        )

    return spotify_artist


def create_spotify_track_instance_from_dict(spotify_track_id: str, spotify_track_dict: dict) -> SpotifyTrack:
    """
    Create a SpotifyTrack instance from a Spotify API response dictionary.

    Args:
        spotify_track_id: The Spotify ID of the track
        spotify_track_dict: The dictionary containing track data from Spotify API

    Returns:
        A SpotifyTrack model instance
    """
    name = spotify_track_dict.get(ApiFields.Names.NAME, "Unknown Track")
    duration_ms = spotify_track_dict.get(ApiFields.Names.DURATION_MS, 0)
    popularity = spotify_track_dict.get(ApiFields.Names.POPULARITY, 0)
    album = spotify_track_dict.get(ApiFields.Names.ALBUM, {})
    preview_url = spotify_track_dict.get(ApiFields.Names.PREVIEW_URL)
    explicit = spotify_track_dict.get(ApiFields.Names.EXPLICIT, False)

    # Try to get existing track or create a new one
    try:
        spotify_track = SpotifyTrack.objects.get(spotify_id=spotify_track_id)
    except ObjectDoesNotExist:
        spotify_track = SpotifyTrack.objects.create(
            spotify_id=spotify_track_id,
            _name=name,
            duration_ms=duration_ms,
            popularity=popularity,
            album=album,
            preview_url=preview_url,
            explicit=explicit
        )

    # Process artists
    artists_data = spotify_track_dict.get(ApiFields.Names.ARTISTS, [])
    if artists_data:
        for artist_data in artists_data:
            artist_id = artist_data.get(ApiFields.Names.ID)
            if artist_id:
                artist = create_spotify_artist_instance_from_dict(artist_id, artist_data)
                spotify_track.spotify_artists.add(artist)

    return spotify_track


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
