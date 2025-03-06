from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_jpeg_then_400(self):
        response = self._post_lib_track(TestLibTrackFilename.FORMAT_IMAGE_JPEG)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID

    def test_mp4_then_400(self):
        response = self._post_lib_track(TestLibTrackFilename.FORMAT_BAD_EXTENSION_MP4)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID
