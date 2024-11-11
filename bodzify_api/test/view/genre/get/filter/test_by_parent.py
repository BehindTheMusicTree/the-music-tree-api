
import logging
from rest_framework import status


from bodzify_api import settings
from bodzify_api.serializer.schema.criteria.output.Fields import Fields as ModelFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_filter_missing_then_return_all_instances(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop", parent=genre_rock)

        response = self._get_genres()

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_filter_empty_then_return_instances_with_no_parent(self):
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop", parent=genre_rock)

        response = self._get_genres(parent='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[ModelFields.NAME] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_rock.name in result_names

    def test_a_parent_uuid_corresponds_then_return_the_children(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_slow = self.model_fixture_factory.create_genre(name="Slow", parent=genre_rock)

        response = self._get_genres(parent=genre_rock.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[ModelFields.NAME] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_slow.name in result_names

    def test_no_parent_uuid_corresponds_then_return_nothing(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genres(parent=genre_punk.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 0
