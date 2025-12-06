from rest_framework import status

from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SpotifyLibTrackFields
from bodzify_api.test.integration.view.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestCase(SpotifyLibTrackTestCase):
    def test_popularity_min_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", popularity=80)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", popularity=60)

        response = self._list_spotify_lib_tracks(popularity_min=70)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track1.name

    def test_popularity_max_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", popularity=80)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", popularity=60)

        response = self._list_spotify_lib_tracks(popularity_max=70)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name

    def test_popularity_range_then_results(self):
        track1 = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", popularity=80)
        track2 = self.model_fixture_factory.create_spotify_lib_track(name="Track 2", popularity=60)
        track3 = self.model_fixture_factory.create_spotify_lib_track(name="Track 3", popularity=40)

        response = self._list_spotify_lib_tracks(popularity_min=50, popularity_max=70)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track2.name
