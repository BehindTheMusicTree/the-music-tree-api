from rest_framework import status
from django.urls import reverse

from api.model.spotify_resource.children.artist.Fields import Fields
from api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestPost(SpotifyArtistTestCase):
    def test_post_spotify_artists_then_405_method_not_allowed(self):
        response = self.api_client.post(
            path=reverse('spotify-artist-list'),
            data={Fields.NAME: 'Test Artist'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
