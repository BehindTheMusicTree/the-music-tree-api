from rest_framework import status

from bodzify_api.serializer.schema.criteria.input.schema.schema import Fields as InputFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_multiple_values_then_error(self):
        response = self._post_genre(kwargs={InputFields.NAME: "Punk", InputFields.PARENT: ["value", "value2"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        response = self._post_genre(kwargs={InputFields.NAME: "Punk", InputFields.PARENT: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_existing(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self._post_genre(kwargs={InputFields.NAME: "Punk", InputFields.PARENT: rock_genre.uuid})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == rock_genre

    def test_error_when_not_existing(self):
        self.model_fixture_factory.create_genre(name="Rock")
        response = self._post_genre(kwargs={InputFields.NAME: "Punk", InputFields.PARENT: "not existing"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
