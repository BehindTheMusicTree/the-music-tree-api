from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenreTestCase):

    def test_extra_field_then_error(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")

        extra_field = "extraField"
        response = self._put_genre(uuid=genre.uuid, **{PostFields.NAME_PUBLIC: "Rock", extra_field: "extra_value"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == extra_field
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.UNKNOWN_FIELD.value
