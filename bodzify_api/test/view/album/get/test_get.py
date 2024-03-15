#!/usr/bin/env python

from ddf import G
from rest_framework import status
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase


class TestCase(ApiTestCase):

    def test(self):
        sum41_artist = G(Artist,
                         name="Sum 41",
                         user=self.test_user)
        G(Album,
            user=self.test_user,
            name="All Killer No Filler",
            year=2001,
            album_artists=[sum41_artist],)
        chuck_album = G(Album,
                        user=self.test_user,
                        name="Chuck",
                        year=2004,
                        album_artists=[sum41_artist],)
        G(LibraryTrack,
            user=self.test_user,
            title="In Too Deep",
            artist=sum41_artist,
            album=chuck_album,
            duration=128)
        G(LibraryTrack,
            user=self.test_user,
            title="We're All To Blame",
            artist=sum41_artist,
            album=chuck_album,
            duration=120)
        G(LibraryTrack,
            user=self.test_user,
            title="Pieces",
            artist=sum41_artist,
            album=chuck_album,
            duration=125)

        response = self.get_albums()
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.overall_total == 2
