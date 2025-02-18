from rest_framework import status

from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenreTestCase):

    def test_no_field_specified_then_error(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_genre(uuid=genre_rock.uuid)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == AppValidationSerializer.REQUEST_FIELD
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.NO_UPDATES.value
