from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils import audio_metadata
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_flac_md5_not_valid_then_corrected(self):
        response = self._post_lib_track_with_specific_sample("md5_not_valid.flac")

        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_object.track_file
        assert track_file
        assert track_file.flac_md5_has_been_corrected
        assert audio_metadata.is_flac_file_md5_valid(track_file.file.path)

    def test_flac_md5_not_valid_and_corrupted_then_error(self):
        response = self._post_lib_track_with_specific_sample("md5_not_valid_and_corrupted.flac")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FILE_CORRUPTED.value

    def test_flac_md5_is_valid(self):
        response = self._post_lib_track_with_specific_sample("md5_valid.flac")

        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_object.track_file
        assert track_file
        assert not track_file.flac_md5_has_been_corrected

    def test_mp3_then_md5_check_is_none(self):
        response = self._post_lib_track_with_specific_sample("sample.mp3")

        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_object.track_file
        assert track_file
        assert not track_file.flac_md5_has_been_corrected
