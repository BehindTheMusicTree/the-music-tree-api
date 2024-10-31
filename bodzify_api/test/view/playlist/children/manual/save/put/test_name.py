
from rest_framework import status

from bodzify_api.model.playlist.BasePlaylist import \
    Fields as BasePlaylistFields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import \
    ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        simpe_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")
        manual_playlist_name_new = "teuf2"
        data = {BasePlaylistFields.NAME: manual_playlist_name_new}
        response = self.put_manual_playlist(
            manual_playlist_uuid=simpe_playlist.base_playlist.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_manual_playlist.name == manual_playlist_name_new

    def test_not_provided_then_unchanged(self):
        manual_playlist_name = "cuisine"
        simpe_playlist = self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        response = self.put_manual_playlist(manual_playlist_uuid=simpe_playlist.base_playlist.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_manual_playlist.name == manual_playlist_name

    def test_empty_then_error(self):
        uuid = self.model_fixture_factory.create_manual_playlist(name='foero').base_playlist.uuid
        data = {BasePlaylistFields.NAME: ""}
        response = self.put_manual_playlist(manual_playlist_uuid=uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
