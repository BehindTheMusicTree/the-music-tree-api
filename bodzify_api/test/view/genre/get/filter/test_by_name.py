
from rest_framework import status


from bodzify_api.serializer.schema.criteria.output.fields import Fields as ModelFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(GenreTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_a_genre_name_contains_the_filter_then_return_it(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='Roc')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][to_camel_case(ModelFields.NAME)] == genre_rock.name

    def test_a_genre_name_contains_the_filter_in_another_case_then_return_it(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop")

        response = self._get_genres(name='RoC')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][to_camel_case(ModelFields.NAME)] == genre_rock.name
