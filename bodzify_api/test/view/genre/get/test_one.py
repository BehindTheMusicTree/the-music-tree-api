
from rest_framework import status

from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_one(self):
        self.model_fixture_factory.create_genre(name="rock")
        response = self._get_genres()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
