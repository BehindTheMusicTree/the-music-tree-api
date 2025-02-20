from django.urls import reverse
from rest_framework import status

from bodzify_api.serializer.model.criteria.input.Fields import Fields as CriteriaPostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestJsonDuplicateFields(GenreTestCase):
    def setUp(self):
        super().setUp()

    def test_duplicate_fields_json_post_then_400(self):
        response = self._post_genre(**{CriteriaPostFields.NAME_PUBLIC: "test", CriteriaPostFields.NAME_PUBLIC: "test2"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_duplicate_fields_on_json_put_then_400(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        datat = {
            CriteriaPostFields.NAME_PUBLIC: "test",
            CriteriaPostFields.NAME_PUBLIC: "test2",
        }
        response = self._put_genre(genre.uuid, **datat)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_duplicate_fields_on_json_patch_then_400(self):
        # PATCH is not supported
        pass
