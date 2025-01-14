from rest_framework import status

from bodzify_api.test.field.filter.char.NullableFreeCharFilterTestCase import NullableFreeCharFilterTestCase
from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase
from bodzify_api.serializer.schema.model.album.fields import Fields as AlbumFields


class TestCase(AlbumTestCase, NullableFreeCharFilterTestCase):

    def test_empty_then_results(self):
        album1 = self.model_fixture_factory.create_album(name="KOKO")
        album2 = self.model_fixture_factory.create_album(name="Kill")
        artist = self.model_fixture_factory.create_artist(name="Muse")
        self.model_fixture_factory.create_album(name="Jon", album_artists=[artist])

        response = self._get_albums(album_artist_name='')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        names = [result[AlbumFields.NAME] for result in self.results]
        assert album1.name in names
        assert album2.name in names

    def test_contains_in_another_case_then_results(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album = self.model_fixture_factory.create_album(name="Dark", album_artists=[artist])
        self.model_fixture_factory.create_album(name="Jon")

        response = self._get_albums(album_artist_name='MUs')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][AlbumFields.NAME] == album.name

    def test_not_provided_then_results(self):
        album1 = self.model_fixture_factory.create_album(name="Dark")
        album2 = self.model_fixture_factory.create_album(name="Jon")

        response = self._get_albums()

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[AlbumFields.NAME] for result in self.results]
        assert album1.name in names
        assert album2.name in names
