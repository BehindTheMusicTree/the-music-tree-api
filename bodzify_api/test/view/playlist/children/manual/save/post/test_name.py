
from rest_framework import status

from bodzify_api.serializer.schema.playlist.children.simple.input.schema import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        data = {Fields.NAME: "a"}
        response = self._post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_then_error(self):
        data = {Fields.NAME: ""}
        response = self._post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_provided_then_error(self):
        response = self._post_manual_playlist(data_dict={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
