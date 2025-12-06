from rest_framework import status
from django.urls import reverse

from bodzify_api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestDelete(SpotifyArtistTestCase):
    def test_delete_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.delete(
            path=reverse('spotify-artist-list')
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
