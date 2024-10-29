#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.album.AlbumTestCase import AlbumTestCase
from bodzify_api.serializer.schema.album.fields import Fields as AlbumFields


class TestCase(AlbumTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_album(name="None")
        self.model_fixture_factory.create_album(name="Kill")
        response = self._get_albums(album_artists_name='')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_a_name_contains_the_filter_then_return_the_album(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album = self.model_fixture_factory.create_album(name="Dark", album_artists=[artist])
        self.model_fixture_factory.create_album(name="Jon")
        response = self._get_albums(album_artists_name='Mus')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][AlbumFields.NAME] == album.name

    def test_a_name_contains_the_filter_in_another_case_then_return_the_album(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album = self.model_fixture_factory.create_album(name="Dark", album_artists=[artist])
        self.model_fixture_factory.create_album(name="Jon")
        response = self._get_albums(album_artists_name='MUs')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][AlbumFields.NAME] == album.name
