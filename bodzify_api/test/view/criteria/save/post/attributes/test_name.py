from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(GenreTestCase):

    def test_not_provided_then_error(self):
        response = self._post_genre(**{})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == PostFields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.REQUIRED.value

    def test_empty_then_error(self):
        response = self._post_genre(**{PostFields.NAME_PUBLIC: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == PostFields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.BLANK.value

    def test_value_then_ok(self):
        name = "rock"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.name == name
