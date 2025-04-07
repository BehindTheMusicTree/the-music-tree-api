from rest_framework import status
from django.urls import reverse

from bodzify_api.test.view.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestPost(SpotifyLibTrackTestCase):
    def setUp(self):
        super().setUp()
        self.track = self.model_fixture_factory.create_spotify_lib_track(
            name="Test Track",
            duration_ms=300000,
            popularity=80,
            album={"name": "Test Album"},
            preview_url="https://example.com/preview",
            explicit=True
        )

    def test_post_spotify_lib_track_then_405_method_not_allowed(self):
        response = self.api_client.post(
            path=reverse('spotify-lib-track-detail', kwargs={'pk': self.track.spotify_id}),
            data={'name': 'Updated Track'}
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
