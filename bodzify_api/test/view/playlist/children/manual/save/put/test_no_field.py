from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_no_field_specified_then_error(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="Kitchen")
        response = self._put_manual_playlist(uuid=manual_playlist.uuid)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
