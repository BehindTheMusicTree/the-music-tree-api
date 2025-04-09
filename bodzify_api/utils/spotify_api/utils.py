from django.core.exceptions import ObjectDoesNotExist

from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.utils.spotify_api.SpotifyClient import SpotifyClient
from bodzify_api.utils.spotify_api.ApiFields import ApiFields
from bodzify_api.utils.spotify_api.managers.SpotifyArtistManager import SpotifyArtistManager

spotify_client = SpotifyClient()
spotify_artist_manager = SpotifyArtistManager()


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
    followers = spotify_lib_track_dict.get(ApiFields.Names.FOLLOWERS, {}).get('total', 0)
    href = spotify_lib_track_dict.get(ApiFields.Names.HREF)
    type = spotify_lib_track_dict.get(ApiFields.Names.TYPE)
    uri = spotify_lib_track_dict.get(ApiFields.Names.URI)

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
            explicit=explicit,
            followers=followers,
            href=href,
            type=type,
            uri=uri
        )

    # Process artists
    artists_data = spotify_lib_track_dict.get(ApiFields.Names.ARTISTS, [])
    if artists_data:
        for artist_data in artists_data:
            artist_id = artist_data.get(ApiFields.Names.ID)
            if artist_id:
                artist = spotify_artist_manager.create_spotify_artist_instance_from_dict(
                    artist_id, artist_data, artist_details)
                spotify_lib_track.spotify_artists.add(artist)

    return spotify_lib_track
