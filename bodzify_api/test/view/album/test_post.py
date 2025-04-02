from rest_framework import status

from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_album(name='test')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
