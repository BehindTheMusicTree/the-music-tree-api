
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.Fields import InputFields as LibTrackInputFields
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_wav_file_corrupted_then_400(self):
        response = self._post_lib_track(LibTrackTestFilename.FORMAT_CORRUPTED_WAV, title="wav corrupted")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == LibTrackInputFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_CORRUPTED
