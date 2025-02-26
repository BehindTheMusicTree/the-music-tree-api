from rest_framework import status

from bodzify_api.serializer.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_not_provided_then_none(self):
        response = self._post_genre(**{PostFields.NAME_PUBLIC: "Rock"})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.parent == None

    def test_empty_then_none(self):
        response = self._post_genre(**{PostFields.NAME_PUBLIC: "Rock", PostFields.PARENT: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.parent == None
