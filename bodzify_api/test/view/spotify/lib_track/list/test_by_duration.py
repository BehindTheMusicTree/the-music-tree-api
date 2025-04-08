from rest_framework import status

from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SpotifyLibTrackFields
from bodzify_api.test.view.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestCase(SpotifyLibTrackTestCase):
    def test_duration_sec_min_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", duration_ms=300000)  # 5 minutes
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", duration_ms=180000)  # 3 minutes

        response = self._list_spotify_lib_tracks(duration_sec_min=240)  # 4 minutes in seconds

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track1.name

    def test_duration_sec_max_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", duration_ms=300000)  # 5 minutes
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", duration_ms=180000)  # 3 minutes

        response = self._list_spotify_lib_tracks(duration_sec_max=210)  # 3.5 minutes in seconds

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name

    def test_duration_range_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", duration_ms=300000)  # 5 minutes
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", duration_ms=180000)  # 3 minutes
        track3 = self.model_fixture_factory.create_spotify_lib_track(name="Track 3", duration_ms=240000)  # 4 minutes

        response = self._list_spotify_lib_tracks(
            duration_sec_min=210, duration_sec_max=270)  # 3.5 to 4.5 minutes in seconds

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track3.name
