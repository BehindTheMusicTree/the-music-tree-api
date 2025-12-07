from rest_framework import status

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.criteria.input.Fields import Fields
from api.test.utils.field.body_data.type.PrimaryCharBodyDataTestCase import PrimaryCharBodyDataTestCase
from api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase, PrimaryCharBodyDataTestCase):

    def test_largest_then_ok(self):
        genre_name = "a" * settings.CRITERIA_NAME_LEN_MAX
        response = self._post_genre(**{Fields.NAME_PUBLIC: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.name == genre_name

    def test_too_large_then_400_bad_request(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "a" * (settings.CRITERIA_NAME_LEN_MAX + 1)})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_multi_value_then_400_bad_request(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: ["value", "value2"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.FORMAT_INVALID

    def test_already_exists_then_400_bad_request(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)

        response = self._post_genre(**{Fields.NAME_PUBLIC: genre_name})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.NAME_DUPLICATE

    def test_empty_then_400_bad_request(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.BLANK

    def test_name_exists_in_another_user_then_ok(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)

        self._login_as_test_user2()
        response = self._post_genre(**{Fields.NAME_PUBLIC: genre_name})
        self._login_as_test_user1()

        assert response.status_code == status.HTTP_201_CREATED
