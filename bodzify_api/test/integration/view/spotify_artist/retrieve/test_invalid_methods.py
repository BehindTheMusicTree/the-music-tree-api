from rest_framework import status
from django.urls import reverse

from bodzify_api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase
from bodzify_api.model.spotify_resource.children.artist.Fields import Fields as ModelFields


class TestInvalidMethods(SpotifyArtistTestCase):
    def setUp(self):
        super().setUp()
        self.artist = self.model_fixture_factory.create_spotify_artist(
            name="Test Artist",
            popularity=90,
            genres=["Rock", "Metal"],
            images=[{"url": "https://example.com/image.jpg"}]
        )

    def test_post_spotify_artist_then_405_method_not_allowed(self):
        response = self.api_client.post(
            path=reverse('spotify-artist-detail', kwargs={'pk': self.artist.spotify_id}),
            data={ModelFields.NAME: 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_spotify_artist_then_405_method_not_allowed(self):
        response = self.api_client.put(
            path=reverse('spotify-artist-detail', kwargs={'pk': self.artist.spotify_id}),
            data={ModelFields.NAME: 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_spotify_artist_then_405_method_not_allowed(self):
        response = self.api_client.patch(
            path=reverse('spotify-artist-detail', kwargs={'pk': self.artist.spotify_id}),
            data={ModelFields.NAME: 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_spotify_artist_then_405_method_not_allowed(self):
        response = self.api_client.delete(
            path=reverse('spotify-artist-detail', kwargs={'pk': self.artist.spotify_id})
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
