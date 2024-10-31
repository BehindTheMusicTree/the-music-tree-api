
from rest_framework import status

from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase


class TestCase(ArtistTestCase):

    def test_filter_not_existing_then_error(self):
        response = self._get_artists(invalid_filter='test')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
