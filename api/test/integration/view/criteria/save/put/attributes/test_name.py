from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.model.track.Track import Track
from api.serializer.model.criteria.input.put import Fields as PutFields
from api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase, PutBodyDataTestCase):

    def test_provided_then_update(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        genre_new_name = "Punk"
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == genre_new_name

    def test_root_name_update(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        assert genre_rock.root.name == "Rock"

        genre_new_name = "Punk"
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})

        assert response.status_code == status.HTTP_200_OK
        updated_genre = self.saved_object
        assert updated_genre.name == genre_new_name
        assert updated_genre.root.name == genre_new_name

    def test_error_when_empty(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PutFields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.BLANK

    def test_not_provided_then_unchanged(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)

        response = self._put_genre(uuid=genre.uuid, **{PutFields.PARENT: None})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == genre_name
