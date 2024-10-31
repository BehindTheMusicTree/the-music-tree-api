
from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.playlist.children.criteria.input.query_param import Fields as GetQueryParams
from bodzify_api.serializer.schema.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Koko")

        response = self._get_genre_playlists(name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_a_name_contains_the_filter_then_return_the_criteria(self):
        criteria = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Punk")

        response = self._get_genre_playlists(name='Ro')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][GetResultFields.NAME] == criteria.name

    def test_a_name_contains_the_filter_then_return_it(self):
        criteria = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Punk")

        response = self._get_genre_playlists(name='RO')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][GetResultFields.NAME] == criteria.name
