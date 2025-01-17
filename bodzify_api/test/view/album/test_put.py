from rest_framework import status

from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_put_then_not_allowed(self):
        album = self.model_fixture_factory.create_album(name='test')
        response = self._put_album(uuid=album.uuid, name='test2')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
