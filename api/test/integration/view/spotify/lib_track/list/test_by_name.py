from rest_framework import status

from api.serializer.model.spotify.lib_track.output.Fields import Fields as SpotifyLibTrackFields
from api.test.utils.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from api.test.integration.view.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestCase(SpotifyLibTrackTestCase, NotNullableFreeCharFilterTestCase):
    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_spotify_lib_track(name="Life")
        self.model_fixture_factory.create_spotify_lib_track(name="Hey")

        response = self._list_spotify_lib_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_400_bad_request(self):
        self.model_fixture_factory.create_spotify_lib_track(name="Life")
        self.model_fixture_factory.create_spotify_lib_track(name="Hey")

        response = self._list_spotify_lib_tracks(name='')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_contains_in_another_case_then_results(self):
        track = self.model_fixture_factory.create_spotify_lib_track(name="LIfe")
        self.model_fixture_factory.create_spotify_lib_track(name="Hey")

        response = self._list_spotify_lib_tracks(name='Lif')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][SpotifyLibTrackFields.NAME] == track.name
