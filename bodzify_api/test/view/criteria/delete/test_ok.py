from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_then_ok(self):
        criteria = self.model_fixture_factory.create_genre(name='criteria')

        response = self._delete_genre(uuid=criteria.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Genre.objects.filter(uuid=criteria.uuid).exists() == False
