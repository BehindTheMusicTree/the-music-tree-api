from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.criteria.input.post import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_multiple_values_then_error(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: ["value", "value2"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_longest_then_ok(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "a" * settings.MANUAL_PLAYLIST_NAME_LEN_MAX})
        assert response.status_code == status.HTTP_201_CREATED

    def test_error_when_too_long(self):
        response = self._post_manual_playlist(
            **{Fields.NAME_PUBLIC: "a" * (settings.MANUAL_PLAYLIST_NAME_LEN_MAX + 1)})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def text_already_exists_then_error(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "value"})
        assert response.status_code == status.HTTP_201_CREATED
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "value"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
