from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_not_provided_then_error(self):
        response = self._post_genre(**{})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_error(self):
        response = self._post_genre(**{PostFields.PARENT: ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_value_then_ok(self):
        name = "rock"
        response = self._post_genre(**{PostFields.NAME: name})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.name == name
