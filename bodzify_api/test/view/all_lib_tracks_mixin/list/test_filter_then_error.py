from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from ..AllLibTracksMixinTestCase import AllLibTracksMixinTestCase


class TestCase(AllLibTracksMixinTestCase):

    def test_filter_then_(self):
        filter = 'filter'
        response = self._get_all_lib_tracks_mixin(**{filter: 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == filter
        assert error['code'] == FieldValidationErrorCode.INVALID_FILTER
