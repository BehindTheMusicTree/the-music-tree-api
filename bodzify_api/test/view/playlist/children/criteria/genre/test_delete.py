
from rest_framework import status

from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import \
    GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_delete_then_not_allowed(self):
        genre = self.model_fixture_factory.create_genre(name='rock')

        response = self._delete_genre_playlist(uuid=genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
