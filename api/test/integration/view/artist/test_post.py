from rest_framework import status

from api.test.integration.view.artist.ArtistTestCase import ArtistTestCase


class TestCase(ArtistTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_artist()
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
