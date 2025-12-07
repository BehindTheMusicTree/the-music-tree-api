from rest_framework import status
from django.urls import reverse

from api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestInvalidMethods(SpotifyArtistTestCase):
    def test_post_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.post(
            path=reverse('spotify-artist-list'),
            data={'name': 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.put(
            path=reverse('spotify-artist-list'),
            data={'name': 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.patch(
            path=reverse('spotify-artist-list'),
            data={'name': 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.delete(
            path=reverse('spotify-artist-list')
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
