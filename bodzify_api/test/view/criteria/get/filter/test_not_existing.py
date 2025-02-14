from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_filter_not_existing_then_error(self):
        response = self._get_lib_tracks(sdkfhsdkjfhskjfh='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == 'sdkfhsdkjfhskjfh'
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.UNKNOWN.value
