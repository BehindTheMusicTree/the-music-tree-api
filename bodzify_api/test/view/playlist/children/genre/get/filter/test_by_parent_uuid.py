
from rest_framework import status

from bodzify_api.serializer.schema.playlist.children.criteria.output.detailed import Fields as GetResultFields
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_filter_is_not_valid_uuid_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genre_playlists(parent='invalid_uuid')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_empty_then_return_genre_without_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock)

        response = self._get_genre_playlists(parent='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1

    def test_criteria_playlist_parent_corresponds_filter_then_return_it(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genre_playlists(parent=genre_rock.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][GetResultFields.NAME] == genre_punk.name
