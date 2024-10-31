
from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import \
    ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_error(self):
        data = {'nonExistingField': 'oifjqoif'}
        response = self.post_manual_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
