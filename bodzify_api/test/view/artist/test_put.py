from rest_framework import status

from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase


class TestCase(ArtistTestCase):

    def test_put_then_error(self):
        artist = self.model_fixture_factory.create_artist(name='mich')
        response = self._put_artist(uuid=artist.uuid)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
