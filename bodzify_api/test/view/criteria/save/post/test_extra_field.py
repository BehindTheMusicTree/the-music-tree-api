from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenreTestCase):

    def test_extra_field_then_error(self):
        extra_field = "extraField"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: "Rock", extra_field: "extra_value"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == extra_field
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.UNKNOWN_FIELD
