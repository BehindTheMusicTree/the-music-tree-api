from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.get_filters.FreeCharFilterTestCase import FreeCharFilterTestCase
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase, FreeCharFilterTestCase):

    def test_empty_then_return_all(self):
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Koko")

        response = self._get_genre_playlists(name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_contains_in_another_case_then_results(self):
        criteria1 = self.model_fixture_factory.create_genre(name="Rock")
        criteria2 = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Punk")

        response = self._get_genre_playlists(name='RO')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[GetResultFields.NAME] for result in self.results]
        assert criteria1.name in result_names
        assert criteria2.name in result_names
