from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_parent_not_provided_then_root_itself(self):
        response = self._post_genre(**{PostFields.NAME: "Rock"})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == self.saved_genre
