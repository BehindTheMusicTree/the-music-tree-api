from rest_framework import status

from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ArtistTestCase):

    def test_filter_not_existing_then_error(self):
        invalid_filter_name = 'invalidFilter'

        response = self._get_artists(**{invalid_filter_name: 'invalidFilter'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == invalid_filter_name
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FILTER.value
