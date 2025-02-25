from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenreTestCase):

    def test_not_provided_then_unchanged(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.NAME_PUBLIC: "New Punk"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.parent == genre_rock

    def test_error_when_parent_is_one_of_descendants(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)

        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.PARENT: punkhardcore_genre.uuid})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PutFields.PARENT
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.ANCESTOR_REFERENCE

    def test_error_when_parent_is_itself(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PutFields.PARENT
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.SELF_REFERENCE
