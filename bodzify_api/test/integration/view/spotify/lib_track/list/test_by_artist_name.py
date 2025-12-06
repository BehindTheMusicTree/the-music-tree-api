from rest_framework import status

from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SpotifyLibTrackFields
from bodzify_api.test.utils.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.integration.view.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestCase(SpotifyLibTrackTestCase, NotNullableFreeCharFilterTestCase):
    def test_not_provided_then_results(self):
        artist1 = self.model_fixture_factory.create_spotify_artist(name="Artist 1")
        artist2 = self.model_fixture_factory.create_spotify_artist(name="Artist 2")
        self.model_fixture_factory.create_spotify_lib_track(name="Track 1", spotify_artists=[artist1])
        self.model_fixture_factory.create_spotify_lib_track(name="Track 2", spotify_artists=[artist2])

        response = self._list_spotify_lib_tracks()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_400_bad_request(self):
        artist1 = self.model_fixture_factory.create_spotify_artist(name="Artist 1")
        artist2 = self.model_fixture_factory.create_spotify_artist(name="Artist 2")
        self.model_fixture_factory.create_spotify_lib_track(name="Track 1", spotify_artists=[artist1])
        self.model_fixture_factory.create_spotify_lib_track(name="Track 2", spotify_artists=[artist2])

        response = self._list_spotify_lib_tracks(album_artist_name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_contains_in_another_case_then_results(self):
        artist1 = self.model_fixture_factory.create_spotify_artist(name="ArTist 1")
        artist2 = self.model_fixture_factory.create_spotify_artist(name="Artist 2")
        track = self.model_fixture_factory.create_spotify_lib_track(name="Track 1", spotify_artists=[artist1])
        self.model_fixture_factory.create_spotify_lib_track(name="Track 2", spotify_artists=[artist2])

        response = self._list_spotify_lib_tracks(album_artist_name='Art')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        assert any(result[SpotifyLibTrackFields.NAME] == track.name for result in self.results)
