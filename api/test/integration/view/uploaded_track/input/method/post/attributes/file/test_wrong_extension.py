from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.post.Fields import Fields as UploadedTrackPostFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_jpeg_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_IMAGE_JPEG)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID

    def test_mp4_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_BAD_EXTENSION_MP4)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID
