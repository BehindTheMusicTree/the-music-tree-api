from rest_framework import status

from api.serializer.model.album.Fields import Fields as AlbumFields
from api.test.utils.field.filter.char.NullableCharFilterTestCase import NullableCharFilterTestCase
from api.test.integration.view.album.AlbumTestCase import AlbumTestCase
from api.filtering.set.album.Fields import Fields as FilterFields


class TestCase(AlbumTestCase, NullableCharFilterTestCase):

    def test_empty_then_results(self):
        album_koko = self.model_fixture_factory.create_album(name="KOKO")
        album_kill = self.model_fixture_factory.create_album(name="Kill")
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album_jon = self.model_fixture_factory.create_album(name="Jon", album_artists=[artist])

        response = self._list_albums(**{FilterFields.ALBUM_ARTIST_NAME: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        names = [result[AlbumFields.NAME_PUBLIC] for result in self.results]
        assert album_koko.name in names
        assert album_kill.name in names
        assert album_jon.name not in names

    def test_contains_in_another_case_then_results(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album = self.model_fixture_factory.create_album(name="Dark", album_artists=[artist])
        self.model_fixture_factory.create_album(name="Jon")

        response = self._list_albums(**{FilterFields.ALBUM_ARTIST_NAME: 'MUs'})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][AlbumFields.NAME_PUBLIC] == album.name

    def test_not_provided_then_results(self):
        album1 = self.model_fixture_factory.create_album(name="Dark")
        album2 = self.model_fixture_factory.create_album(name="Jon")

        response = self._list_albums()

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[AlbumFields.NAME_PUBLIC] for result in self.results]
        assert album1.name in names
        assert album2.name in names
