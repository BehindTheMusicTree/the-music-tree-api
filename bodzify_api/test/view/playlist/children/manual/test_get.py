from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_get_then_ok(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name='foot')
        response = self._get_manual_playlists(uuid=manual_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
