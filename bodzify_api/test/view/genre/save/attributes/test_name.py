from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields
from bodzify_api.test.get_filters.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase, NotNullableFreeCharFilterTestCase):

    def test_longest(self):
        genre_name = "a" * settings.CRITERIA_NAME_LEN_MAX
        response = self._post_genre(**{Fields.NAME: genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.name == genre_name

    def test_error_too_long(self):
        response = self._post_genre(**{Fields.NAME: "a" * (settings.CRITERIA_NAME_LEN_MAX + 1)})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_multiple_values_then_error(self):
        response = self._post_genre(**{Fields.NAME: ["value", "value2"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_already_exists_then_error(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        response = self._post_genre(**{Fields.NAME: genre_name})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
