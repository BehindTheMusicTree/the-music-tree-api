import os
from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_jpeg_then_400(self):
        response = self._post_lib_track(LibTrackTestFilename.FORMAT_IMAGE_JPEG)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID

    def test_temp_file_removed_on_400(self):
        """Test that temporary files are cleaned up when a request fails with 400."""
        # Make a request that will fail validation
        response = self._post_lib_track(LibTrackTestFilename.FORMAT_IMAGE_JPEG)

        # Get the temp file from the request
        temp_file = response.wsgi_request.FILES[LibTrackPostFields.TRACK_FILE_PUBLIC]
        if not isinstance(temp_file, TemporaryUploadedFile):
            self.fail("Expected TemporaryUploadedFile")

        temp_path = temp_file.temporary_file_path()

        # Verify the response was a 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify the temp file was cleaned up
        self.assertFalse(os.path.exists(temp_path), "Temporary file was not cleaned up")
