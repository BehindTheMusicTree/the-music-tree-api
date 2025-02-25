from rest_framework import status

from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import \
    GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_put_then_not_allowed(self):
        genre = self.model_fixture_factory.create_genre(name='genre')

        response = self._put_genre_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
