import pytest

from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_jpeg_then_error(self):
        response = self._post_lib_track_with_specific_sample("image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.INVALID_FILE_TYPE

    def test_mp4_then_error(self):
        response = self._post_lib_track_with_specific_sample("bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.INVALID_FILE_TYPE
