from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.output.Fields import Fields as ModelFields
from bodzify_api.test.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(GenreTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_contains_in_another_case_then_results(self):
        genre_rock1 = self.model_fixture_factory.create_genre(name="Rock")
        genre_rock2 = self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='RoC')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[to_camel_case(ModelFields.NAME)] for result in self.results]
        assert genre_rock1.name in result_names
        assert genre_rock2.name in result_names

    def test_not_provided_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_pop = self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[to_camel_case(ModelFields.NAME)] for result in self.results]
        assert genre_rock.name in result_names
        assert genre_pop.name in result_names
