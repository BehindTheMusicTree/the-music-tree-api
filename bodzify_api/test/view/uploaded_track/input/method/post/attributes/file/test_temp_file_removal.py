import os
from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_uploaded_track_created_then_temp_dir_empty(self):
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

        response = self._post_uploaded_track(UploadedTrackTestFilename.DEFAULT_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

    def test_uploaded_track_post_in_400_then_temp_dir_empty(self):
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_CORRUPTED_WAV)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []
