from rest_framework import status

from bodzify_api.serializer.schema.model.artist.fields import Fields as ArtistFields
from bodzify_api.test.get_filters.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(ArtistTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        response = self._get_artists(name='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_contains_in_another_case_then_results(self):
        artist1 = self.model_fixture_factory.create_artist(name="Muse")
        artist2 = self.model_fixture_factory.create_artist(name="Museum")
        self.model_fixture_factory.create_artist(name="Jon")
        response = self._get_artists(name='MUs')
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[to_camel_case(ArtistFields.NAME)] for result in self.results]
        assert artist1.name in result_names
        assert artist2.name in result_names
