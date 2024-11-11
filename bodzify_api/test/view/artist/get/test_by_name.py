from rest_framework import status

from bodzify_api.serializer.schema.artist.fields import Fields as ArtistFields
from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(ArtistTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_artist(name="Muse")
        self.model_fixture_factory.create_artist(name="Museum")
        self.model_fixture_factory.create_artist(name="Sum")
        response = self._get_artists(name='')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3

    def test_names_contain_the_filter_then_return_the_instances(self):
        artist1 = self.model_fixture_factory.create_artist(name="Muse")
        artist2 = self.model_fixture_factory.create_artist(name="Museum")
        response = self._get_artists(name='Mus')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[to_camel_case(ArtistFields.NAME)] for result in self.results]
        assert artist1.name in result_names
        assert artist2.name in result_names

    def test_a_name_contains_the_filter_in_another_case_then_return_the_instance(self):
        artist1 = self.model_fixture_factory.create_artist(name="Muse")
        artist2 = self.model_fixture_factory.create_artist(name="Museum")
        self.model_fixture_factory.create_artist(name="Jon")
        response = self._get_artists(name='MUs')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        result_names = [result[to_camel_case(ArtistFields.NAME)] for result in self.results]
        assert artist1.name in result_names
        assert artist2.name in result_names
