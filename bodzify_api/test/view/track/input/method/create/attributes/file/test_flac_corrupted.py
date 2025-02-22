from unittest.mock import patch

from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.audio_metadata.exceptions import FlacMd5CheckFailedError
from bodzify_api.serializer.model.lib_track.input.Fields import Fields as LibTrackInputFields
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_flac_file_corrupted_then_400(self):
        with patch('bodzify_api.utils.audio_metadata.replace_flac_file_with_corrected_md5') as mock_replace_flac_file_with_corrected_md5:
            exception_message = \
                "The FLAC file MD5 check failed and could not be corrected. The file is probably corrupted."
            mock_replace_flac_file_with_corrected_md5.side_effect = FlacMd5CheckFailedError(exception_message)

            response = self._post_lib_track_with_generic_sample_no_tags(extension='flac')

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert len(self.bad_request_result_field_errors) == 1
            error = self.bad_request_result_field_errors[0]
            assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackInputFields.TRACK_FILE_PUBLIC
            assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FILE_CORRUPTED.value
