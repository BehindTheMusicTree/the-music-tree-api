from rest_framework import status
from django.urls import reverse

from bodzify_api.model.spotify_resource.children.artist.Fields import Fields
from bodzify_api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestPut(SpotifyArtistTestCase):
    def test_put_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.put(
            path=reverse('spotify-artist-list'),
            data={Fields.NAME: 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
