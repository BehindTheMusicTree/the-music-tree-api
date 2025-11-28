from rest_framework import status
from django.urls import reverse

from bodzify_api.test.view.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestPut(SpotifyLibTrackTestCase):
    def test_put_spotify_lib_tracks_then_405_method_not_allowed(self):
        response = self.api_client.put(
            path=reverse('spotify-lib-track-list'),
            data={'name': 'Test Track'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
