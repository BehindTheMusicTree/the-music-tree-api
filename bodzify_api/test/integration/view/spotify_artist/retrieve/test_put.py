from rest_framework import status
from django.urls import reverse

from bodzify_api.model.spotify_resource.children.artist.Fields import Fields
from bodzify_api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestPut(SpotifyArtistTestCase):
    def setUp(self):
        super().setUp()
        self.artist = self.model_fixture_factory.create_spotify_artist(
            name='Test Artist',
            popularity=90,
            genres=['rock', 'pop'],
            images=[{'url': 'https://example.com/image.jpg', 'height': 640, 'width': 640}]
        )

    def test_put_spotify_artist_then_405_method_not_allowed(self):
        response = self.api_client.put(
            path=reverse('spotify-artist-detail', kwargs={'pk': self.artist.pk}),
            data={Fields.NAME: 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
