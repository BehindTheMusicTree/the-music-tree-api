import os
from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_lib_track_created_then_temp_dir_empty(self):
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

        response = self._post_lib_track(LibTrackTestFilename.DEFAULT_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

    def test_lib_track_post_in_400_then_temp_dir_empty(self):
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

        response = self._post_lib_track(LibTrackTestFilename.DEFAULT_MP3,
                                        status_code_expected=status.HTTP_400_BAD_REQUEST)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []
