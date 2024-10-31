
from rest_framework import status


from bodzify_api.serializer.schema.criteria.output.fields import Fields as ModelFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_filter_empty_then_return_genre_with_no_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop", parent=genre_rock)

        response = self._get_genres(parent='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][ModelFields.NAME] == genre_rock.name

    # def test_a_parent_name_contains_the_filter_then_return_it(self):
    #     genre_rock = self.model_fixture_factory.create_genre(name="Rock")
    #     genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

    #     response = self._get_genres(parent='Roc')

    #     assert response.status_code == status.HTTP_200_OK
    #     assert self.overall_total == 1
    #     assert self.results[0][ModelFields.NAME] == genre_punk.name

    # def test_a_parent_name_contains_the_filter_in_another_case_then_return_it(self):
    #     genre_rock = self.model_fixture_factory.create_genre(name="Rock")
    #     genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

    #     response = self._get_genres(parent='RoC')

    #     assert response.status_code == status.HTTP_200_OK
    #     assert self.overall_total == 1
    #     assert self.results[0][ModelFields.NAME] == genre_punk.name
