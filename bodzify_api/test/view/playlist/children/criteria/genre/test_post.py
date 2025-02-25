from rest_framework import status

from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import \
    GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_genre_playlist()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
