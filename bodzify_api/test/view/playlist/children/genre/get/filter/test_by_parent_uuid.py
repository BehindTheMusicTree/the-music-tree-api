from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.field.filter.foreign_key.PrivateForeignKeyFilterTestCase import PrivateForeignKeyFilterTestCase
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase, PrivateForeignKeyFilterTestCase):

    def setUp(self, methods_names_to_implement=None):
        return super().setUp(allow_empty_value=True, methods_names_to_implement=methods_names_to_implement)

    def test_not_provided_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock)

        response = self._get_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 4

    def test_invalid_uuid_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genre_playlists(**{GetResultFields.PARENT: 'invalid-uuid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock.criteria_playlist)

        response = self._get_genre_playlists(**{GetResultFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[GetResultFields.NAME] for result in self.results]
        assert genre_rock.name in result_names
        assert genre_rockabilly.name in result_names

    def test_genres_playlist_parent_corresponds_to_filter_then_return_instances(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly", parent=genre_rock)
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genre_playlists(**{GetResultFields.PARENT: genre_rock.criteria_playlist.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[GetResultFields.NAME] for result in self.results]
        assert genre_rockabilly.name in result_names
        assert genre_punk.name in result_names
