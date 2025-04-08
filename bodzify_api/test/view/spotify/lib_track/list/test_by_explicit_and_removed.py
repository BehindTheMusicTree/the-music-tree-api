from rest_framework import status

from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SpotifyLibTrackFields
from bodzify_api.test.view.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestCase(SpotifyLibTrackTestCase):
    def test_explicit_true_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", explicit=True)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", explicit=False)

        response = self._list_spotify_lib_tracks(explicit=True)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track1.name

    def test_explicit_false_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", explicit=True)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", explicit=False)

        response = self._list_spotify_lib_tracks(explicit=False)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name

    def test_is_removed_true_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", is_removed=True)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", is_removed=False)

        response = self._list_spotify_lib_tracks(is_removed=True)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track1.name

    def test_is_removed_false_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", is_removed=True)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", is_removed=False)

        response = self._list_spotify_lib_tracks(is_removed=False)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name
