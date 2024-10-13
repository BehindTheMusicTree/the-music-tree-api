#!/usr/bin/env python

from rest_framework import status


from bodzify_api.serializer.artist.detailed import Fields as ArtistFields
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(ArtistViewTestCase):

    def test_duration(self):
        artist = self.model_fixture_factory.create_artist(name="Sum 41")
        track_intodeep = self.model_fixture_factory.create_lib_track(title="In Too Deep", artists=[artist])
        track_summer = self.model_fixture_factory.create_lib_track(title="Summer", artists=[artist])
        tracks_duration_in_sec = track_intodeep.duration_in_sec + track_summer.duration_in_sec  # type: ignore
        response = self._retrieve(artist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(ArtistFields.DURATION_IN_SEC)] == tracks_duration_in_sec

    def test_count(self):
        artist = self.model_fixture_factory.create_artist(name="Sum 41")
        self.model_fixture_factory.create_lib_track(title="In Too Deep", artists=[artist])
        self.model_fixture_factory.create_lib_track(title="Summer", artists=[artist])
        response = self._retrieve(artist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(ArtistFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        artist = self.model_fixture_factory.create_artist(name="Sum 41")
        self.model_fixture_factory.create_lib_track(title="In Too Deep", artists=[artist])
        self.model_fixture_factory.create_lib_track(title="Summer", artists=[artist], archived=True)
        self.model_fixture_factory.create_lib_track(title="Summer2", artists=[artist], archived=True)
        self.model_fixture_factory.create_lib_track(title="Summer3", artists=[artist], archived=True)
        response = self._retrieve(artist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(ArtistFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
