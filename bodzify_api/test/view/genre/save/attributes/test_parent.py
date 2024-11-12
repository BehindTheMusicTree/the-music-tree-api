from rest_framework import status

from bodzify_api.serializer.schema.criteria.input.schema.schema import Fields as InputFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_multiple_values_then_error(self):
        data = {
            InputFields.NAME: "Punk",
            InputFields.PARENT: ["value", "value2"]
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        data = {
            InputFields.NAME: "Punk",
            InputFields.PARENT: ""
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_existing(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        data = {
            InputFields.NAME: "Punk",
            InputFields.PARENT: rock_genre.uuid
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == rock_genre

    def test_error_when_not_existing(self):
        self.model_fixture_factory.create_genre(name="Rock")
        data = {
            InputFields.NAME: "Punk",
            InputFields.PARENT: "not existing"
        }
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
