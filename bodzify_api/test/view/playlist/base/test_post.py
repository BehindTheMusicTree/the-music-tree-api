from rest_framework import status

from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase


class TestCase(BasePlaylistTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_base_playlist()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
