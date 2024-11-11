from rest_framework import status

from bodzify_api.serializer.schema.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_filter_is_not_valid_uuid_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genre_playlists(parent='invalid_uuid')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_empty_then_return_genre_playlists_without_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock.criteria_playlist)

        response = self._get_genre_playlists(parent='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[GetResultFields.NAME] for result in self.results]
        assert genre_rock.name in result_names
        assert genre_rockabilly.name in result_names

    def test_genres_playlist_parent_corresponds_to_filter_then_return_instances(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly", parent=genre_rock)
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genre_playlists(parent=genre_rock.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[GetResultFields.NAME] for result in self.results]
        assert genre_rockabilly.name in result_names
        assert genre_punk.name in result_names
