from rest_framework import status
from django.urls import reverse

from api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestDelete(SpotifyArtistTestCase):
    def setUp(self):
        super().setUp()
        self.artist = self.model_fixture_factory.create_spotify_artist(
            name='Test Artist',
            popularity=90,
            genres=['rock', 'pop'],
            images=[{'url': 'https://example.com/image.jpg', 'height': 640, 'width': 640}]
        )

    def test_delete_spotify_artist_then_405_method_not_allowed(self):
        response = self.api_client.delete(
            path=reverse('spotify-artist-detail', kwargs={'pk': self.artist.pk})
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
