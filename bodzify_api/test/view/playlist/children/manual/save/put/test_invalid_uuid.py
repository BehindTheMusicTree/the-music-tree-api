from uuid import UUID

from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_invalid_uuid_then_404(self):
        response = self._put_manual_playlist(uuid=UUID('ee8f5054-cd30-4d59-ba15-997a00a9a033'))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_malformed_uuid_then_400_bad_request(self):
        response = self._put_manual_playlist(uuid="invalid_uuid")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
