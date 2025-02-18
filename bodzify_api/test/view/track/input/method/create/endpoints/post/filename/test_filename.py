from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_ok_when_max_length(self):
        sample_150_char_long_char_name = ("kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2" +
                                          "ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAF" +
                                          "RnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd5.mp3")
        response = self._post_lib_track_with_specific_sample(
            specific_sample_filename=sample_150_char_long_char_name, **{})

        assert response.status_code == status.HTTP_201_CREATED

    def test_error_when_too_long(self):
        sample_151_char_long_char_name = ("kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2" +
                                          "ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAF" +
                                          "RnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd51.mp3")
        response = self._post_lib_track_with_specific_sample(
            specific_sample_filename=sample_151_char_long_char_name, **{})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.INVALID_FILENAME
