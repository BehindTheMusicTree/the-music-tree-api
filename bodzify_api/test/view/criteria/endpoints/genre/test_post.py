from rest_framework import status

from bodzify_api.serializer.model.criteria.input.post import     Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_ok(self):
        genre_name = "rock"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.name == genre_name
