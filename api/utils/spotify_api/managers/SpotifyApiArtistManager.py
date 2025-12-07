from django.core.exceptions import ObjectDoesNotExist

from api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from api.utils.spotify_api.SpotifyClient import SpotifyClient
from api.utils.spotify_api.ApiFields import ApiFields


class SpotifyApiArtistManager:
    def __init__(self):
        self.spotify_client = SpotifyClient()

    def batch_fetch_artist_details(self, artist_ids: list[str], user) -> dict[str, dict]:
        """
        Fetch details for multiple artists in batches of 50 (Spotify's limit).

        Args:
            artist_ids: List of Spotify artist IDs
            user: User instance to check Spotify authentication

        Returns:
            Dictionary mapping artist IDs to their full details
        """
        artist_details = {}

        # Process in batches of 50 (Spotify's limit)
        batch_size = 50
        for i in range(0, len(artist_ids), batch_size):
            batch = artist_ids[i:i + batch_size]
            try:
                # Fetch all artists in the batch
                results = self.spotify_client.spotify.artists(batch)
                if results and 'artists' in results:
                    for artist in results['artists']:
                        if artist:  # Skip any None results
                            artist_details[artist['id']] = artist
            except Exception as e:
                print(f"Error fetching artist batch: {str(e)}")
                # Continue with next batch even if one fails

        return artist_details

    def create_spotify_artist_instance_from_dict(
            self, spotify_artist_id: str, spotify_artist_dict: dict, artist_details: dict | None = None) -> SpotifyArtist:
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
