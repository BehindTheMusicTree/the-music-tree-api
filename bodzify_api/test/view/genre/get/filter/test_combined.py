from rest_framework import status

from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.utils.utils import to_camel_case
from bodzify_api.serializer.schema.criteria.output.Fields import Fields as GenreFields


class TestCase(GenreTestCase):

    def test_name_and_parent_name_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pure Pop")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genres(name='pu', parent=genre_rock.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][to_camel_case(GenreFields.NAME)] == genre_punk.name
