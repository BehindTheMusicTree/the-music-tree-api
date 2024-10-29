#!/usr/bin/env python

from rest_framework import status


from bodzify_api.serializer.schema.artist.fields import Fields as ArtistFields
from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(ArtistTestCase):

    def test_filter_empty_then_return_all(self):
        self.model_fixture_factory.create_artist(name="Muse")
        self.model_fixture_factory.create_artist(name="Sum")
        response = self._get_artists(name='')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_a_name_contains_the_filter_then_return_the_artist(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        self.model_fixture_factory.create_artist(name="Jon")
        response = self._get_artists(name='Mus')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][to_camel_case(ArtistFields.NAME)] == artist.name

    def test_a_name_contains_the_filter_then_return_it(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        self.model_fixture_factory.create_artist(name="Jon")
        response = self._get_artists(name='MUs')
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 1
        assert self.results[0][to_camel_case(ArtistFields.NAME)] == artist.name
