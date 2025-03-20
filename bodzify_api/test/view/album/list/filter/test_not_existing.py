
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase


class TestCase(AlbumTestCase):

    def test_filter_not_existing_then_400(self):
        invalid_filter = 'invalidFilter'
        response = self._list_albums(**{invalid_filter: 'value'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == invalid_filter
        assert error['code'] == FieldValidationErrorCode.INVALID_FILTER
