from rest_framework import status

from bodzify_api.model.criteria.Criteria import Fields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_ok(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)
        response = self._get_genres()
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        genre_rock_json = self.results[0]
        assert genre_rock_json[Fields.NAME_PUBLIC] == genre_name
