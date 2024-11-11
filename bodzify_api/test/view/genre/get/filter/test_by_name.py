from rest_framework import status

from bodzify_api.serializer.schema.criteria.output.Fields import Fields as ModelFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(GenreTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_genre_names_contain_the_filter_then_return_the_instances(self):
        genre_rock1 = self.model_fixture_factory.create_genre(name="Rock")
        genre_rock2 = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='Roc')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[to_camel_case(ModelFields.NAME)] for result in self.results]
        assert genre_rock1.name in result_names
        assert genre_rock2.name in result_names

    def test_genre_names_contains_the_filter_in_another_case_then_return_the_instances(self):
        genre_rock1 = self.model_fixture_factory.create_genre(name="Rock")
        genre_rock2 = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='RoC')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[to_camel_case(ModelFields.NAME)] for result in self.results]
        assert genre_rock1.name in result_names
        assert genre_rock2.name in result_names
