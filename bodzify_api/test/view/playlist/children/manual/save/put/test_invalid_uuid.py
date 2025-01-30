from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_invalid_uuid_then_404(self):
        response = self._put_manual_playlist(uuid="invalid_uuid")
        assert response.status_code == status.HTTP_404_NOT_FOUND
