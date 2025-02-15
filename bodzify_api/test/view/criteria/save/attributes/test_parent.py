from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as Fields
from bodzify_api.test.field.body_data.type.NullableBodyDataTestCase import NullableBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(GenreTestCase, NullableBodyDataTestCase):

    def test_multiple_values_then_error(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: ["value", "value2"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.PARENT
        assert error['code'] == FieldValidationErrorCode.UNEXPECTED_LIST_VALUE.value

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
        print('error', error)
        assert error['field'] == Fields.PARENT
        assert error['code'] == FieldValidationErrorCode.RESOURCE_NOT_OWNED.value
