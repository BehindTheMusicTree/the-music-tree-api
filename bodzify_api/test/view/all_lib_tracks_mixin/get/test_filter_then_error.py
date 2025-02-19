from rest_framework import status

from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields

from ..AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_filter_then_error(self):
        filter = 'filter'
        response = self._get_all_lib_tracks_mixin(kwargs={filter: 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == filter
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.BLANK.value
