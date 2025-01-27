from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.manual.input.schema import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "a"})
        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_then_error(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_provided_then_error(self):
        response = self._post_manual_playlist(**{})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
