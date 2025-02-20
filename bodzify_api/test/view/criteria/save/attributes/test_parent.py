from rest_framework import status

from bodzify_api.serializer.model.criteria.input.Fields import Fields as Fields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.test.utils.field.body_data.type.to_extend_from.ForeignKeyBodyDataTestCase \
    import ForeignKeyBodyDataTestCase


class TestCase(GenreTestCase, ForeignKeyBodyDataTestCase):

    def test_multiple_values_then_error(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: ["value", "value2"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == Fields.PARENT
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.UNEXPECTED_LIST.value

    def test_empty_then_none(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.parent == None

    def test_existing_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.parent == genre_rock

    def test_non_existing_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._post_genre(
            **{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: "5d63bbee-32ca-47d9-89fe-fd82f18dd183"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == Fields.PARENT
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_REFERENCE.value
