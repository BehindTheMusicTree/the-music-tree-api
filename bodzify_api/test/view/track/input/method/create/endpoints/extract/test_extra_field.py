from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(LibTrackTestCase):

    def test_extra_field_then_error(self):
        response = self._extract_default_mine_track(**{"field_not_handled": "pofkefposkfwp"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == "field_not_handled"
        assert error['code'] == FieldValidationErrorCode.INVALID_REFERENCE
