from rest_framework import status

from bodzify_api.model.criteria.Criteria import Fields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.serializer.schema.criteria.output.Fields import Fields as GetFields


class TestCase(GenreTestCase):

    def test_name(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        response = self._get_genres()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        rock_genre_json = self.results[0]
        assert rock_genre_json[Fields.NAME] == genre_name
