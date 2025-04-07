from rest_framework import status

from bodzify_api.test.view.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestGet(SpotifyLibTrackTestCase):
    def test_list_spotify_lib_tracks_then_ok(self):
        response = self._list_spotify_lib_tracks()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['results']) == 0

    def test_list_spotify_lib_tracks_with_filter_then_ok(self):
        response = self._list_spotify_lib_tracks(name="Test")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['results']) == 0
