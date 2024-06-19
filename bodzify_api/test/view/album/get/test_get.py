#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase


class TestCase(AlbumViewTestCase):

    def test_get(self):
        sum41_artist = self.model_fixture_factory.create_artist(name="Sum 41")
        allkiller_album = self.model_fixture_factory.create_album(
            name="All Killer No Filler", year=2001, album_artists=[sum41_artist],)
        chuck_album = self.model_fixture_factory.create_album(name="Chuck", year=2004, album_artists=[sum41_artist])
        self.model_fixture_factory.create_lib_track(title="In Too Deep", artist=sum41_artist, album=chuck_album)
        self.model_fixture_factory.create_lib_track(title="We're All To Blame", artist=sum41_artist, album=chuck_album)
        self.model_fixture_factory.create_lib_track(title="Pieces", artist=sum41_artist, album=allkiller_album)
        response = self.get_albums()
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
