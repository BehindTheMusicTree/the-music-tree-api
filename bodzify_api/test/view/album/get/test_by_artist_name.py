from rest_framework import status

from bodzify_api.test.get_filters.FreeCharFilterTestCase import FreeCharFilterTestCase
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase
from bodzify_api.serializer.schema.model.album.fields import Fields as AlbumFields


class TestCase(AlbumTestCase, FreeCharFilterTestCase):

    def test_empty_then_return_all(self):
        self.model_fixture_factory.create_album(name="None")
        self.model_fixture_factory.create_album(name="Kill")

        response = self._get_albums(album_artists_name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_contains_in_another_case_then_results(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album = self.model_fixture_factory.create_album(name="Dark", album_artists=[artist])
        self.model_fixture_factory.create_album(name="Jon")

        response = self._get_albums(album_artists_name='MUs')

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][AlbumFields.NAME] == album.name

    def test_empty_then_error(self):
        response = self._get_albums(album_artists_name='')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_provided_then_results(self):
        album1 = self.model_fixture_factory.create_album(name="Dark")
        album2 = self.model_fixture_factory.create_album(name="Jon")

        response = self._get_albums()

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[AlbumFields.NAME] for result in self.results]
        assert album1.name in names
        assert album2.name in names
