from uuid import UUID

from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_post_then_not_allowed(self):
        response = self._delete_manual_playlist(uuid=UUID('00000000-0000-0000-0000-000000000000'))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
