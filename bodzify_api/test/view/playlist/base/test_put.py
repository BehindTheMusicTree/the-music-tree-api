from rest_framework import status

from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase


class TestCase(PlaylistTestCase):

    def test_put_then_error(self):
        genre = self.model_fixture_factory.create_genre(name='genre')
        response = self._delete_playlist(uuid=genre.criteria_playlist.uuid)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
