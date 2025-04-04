from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TextCase(LibTrackTestCase):

    def test_random_then_ok(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
