
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.Fields import Fields as UploadedTrackInputFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_wav_file_corrupted_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_CORRUPTED_WAV, title="wav corrupted")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackInputFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_CORRUPTED
