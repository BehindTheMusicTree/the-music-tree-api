from rest_framework import status

from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.filtering.set.playlist.Fields import Fields as FilterFields
from bodzify_api.test.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genre_playlists(**{FilterFields.NAME: ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_tag_playlists_then_not_in_results(self):
        tag = self.model_fixture_factory.create_tag(name="foot")
        genre = self.model_fixture_factory.create_genre(name="foot rock")

        response = self._get_genre_playlists(**{FilterFields.NAME: 'foot'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre.name in result_names
        assert tag.name not in result_names

    def test_contains_in_another_case_then_results(self):
        criteria1 = self.model_fixture_factory.create_genre(name="Rock")
        criteria2 = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Punk")

        response = self._get_genre_playlists(**{FilterFields.NAME: 'RO'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert criteria1.name in result_names
        assert criteria2.name in result_names

    def test_not_provided_then_results(self):
        criteria1 = self.model_fixture_factory.create_genre(name="Rock")
        criteria2 = self.model_fixture_factory.create_genre(name="Rockabilly")
        criteria3 = self.model_fixture_factory.create_genre(name="Punk")

        response = self._get_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 4
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert criteria1.name in result_names
        assert criteria2.name in result_names
        assert criteria3.name in result_names

    def test_name_in_genreless_and_criteria_name_then_results(self):
        genre_genre = self.model_fixture_factory.create_genre(name="genre")
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genre_playlists(**{FilterFields.NAME: 'geN'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre_genre.name in result_names
        assert genre_rock.name not in result_names
        genreless_playlist: GenrePlaylist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        assert genreless_playlist.name in result_names
