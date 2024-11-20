from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_error(self):
        response = self._post_manual_playlist(**{'nonExistingField': 'oifjqoif'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
