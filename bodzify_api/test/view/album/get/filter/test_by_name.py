from rest_framework import status

from bodzify_api.test.field.filter.char.NotNullableFreeCharFilterTestCase import NotNullableFreeCharFilterTestCase
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase
from bodzify_api.serializer.schema.model.album.Fields import Fields as AlbumFields


class TestCase(AlbumTestCase, NotNullableFreeCharFilterTestCase):

    def test_empty_then_error(self):
        response = self._get_albums(name='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_contains_in_another_case_then_results(self):
        album = self.model_fixture_factory.create_album(name="Muse")
        self.model_fixture_factory.create_album(name="Jon")
        response = self._get_albums(name='MUs')
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][AlbumFields.NAME] == album.name

    def test_not_provided_then_results(self):
        self.model_fixture_factory.create_album(name="Muse")
        self.model_fixture_factory.create_album(name="Jon")
        response = self._get_albums()
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
