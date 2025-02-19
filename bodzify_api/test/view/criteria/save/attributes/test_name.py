from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields
from bodzify_api.test.field.body_data.method.SaveBodyDataTestCase import SaveBodyDataTestCase
from bodzify_api.test.field.body_data.type.not_nullable.PrimaryBodyDataTestCase import PrimaryBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenreTestCase, PrimaryBodyDataTestCase, SaveBodyDataTestCase):

    def test_longest_then_ok(self):
        genre_name = "a" * settings.CRITERIA_NAME_LEN_MAX
        response = self._post_genre(**{Fields.NAME_PUBLIC: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.name == genre_name

    def test_too_long_then_error(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "a" * (settings.CRITERIA_NAME_LEN_MAX + 1)})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.STRING_TOO_LONG.value

    def test_multiple_values_then_error(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: ["value", "value2"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.UNEXPECTED_LIST.value

    def test_already_exists_then_error(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)

        response = self._post_genre(**{Fields.NAME_PUBLIC: genre_name})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.NAME_DUPLICATE.value

    def test_empty_then_error(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.BLANK.value
