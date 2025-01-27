from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as Fields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase, NullableFieldTestCase):

    def test_multiple_values_then_error(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: ["value", "value2"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_existing(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == genre_rock

    def test_error_when_not_existing(self):
        self.model_fixture_factory.create_genre(name="Rock")
        response = self._post_genre(**{Fields.NAME_PUBLIC: "Punk", Fields.PARENT: "not existing"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
