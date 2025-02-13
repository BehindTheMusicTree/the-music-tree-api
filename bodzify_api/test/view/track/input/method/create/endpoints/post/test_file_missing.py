import pytest
from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_missing_then_error(self):
        response = self._post_lib_track_without_file()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.REQUIRED
