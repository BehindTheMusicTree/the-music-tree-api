from rest_framework import status

from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.serializer.schema.criteria.output.Fields import Fields as GenreFields


class TestCase(GenreTestCase):

    def test_name_and_parent_uuid_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pure Pop")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_punky = self.model_fixture_factory.create_genre(name="Punky", parent=genre_rock)

        response = self._get_genres(name='pu', parent=genre_rock.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[to_camel_case(GenreFields.NAME)] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_punky.name in result_names
