from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from bodzify_api.serializer.model.criteria.output.Fields import Fields as GenreFields
from bodzify_api.test.integration.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class TestCase(GenreTestCase):

    def test_name_and_parent_uuid_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pure Pop")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_punky = self.model_fixture_factory.create_genre(name="Punky", parent=genre_rock)

        response = self._list_genres(name='pu', parent=genre_rock.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[to_camel_case(GenreFields.NAME)] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_punky.name in result_names

    def test_name_and_updated_on_range_then_ok(self):
        now = timezone.now()
        past = now - timedelta(days=5)
        future = now + timedelta(days=5)

        # Create genres with different updated_on dates
        genre_rock_new = self.model_fixture_factory.create_genre(
            name="Rock", updated_on=now)
        genre_rock_old = self.model_fixture_factory.create_genre(
            name="Rock Alternative", updated_on=past)
        self.model_fixture_factory.create_genre(
            name="Rock Future", updated_on=future)
        self.model_fixture_factory.create_genre(
            name="Pop", updated_on=now)

        response = self._list_genres(
            name='Rock',
            **{
                PrivateUniqueResourceFields.UPDATED_ON_GTE: past.isoformat(),
                PrivateUniqueResourceFields.UPDATED_ON_LTE: now.isoformat()
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[to_camel_case(GenreFields.NAME)] for result in self.results]
        assert genre_rock_new.name in result_names
        assert genre_rock_old.name in result_names
