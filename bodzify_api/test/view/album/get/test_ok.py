#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase, RESPONSE_KEYS

class TestCase(ApiViewTestCase):

    def test(self):
        sum41Artist = G(Artist,
                        name="Sum 41",
                        user=self.test_user)
        G(Album, 
            user=self.test_user,
            name="All Killer No Filler",
            year=2001,
            album_artists=[sum41Artist],)
        chuckAlbum = G(Album, 
                        user=self.test_user,
                        name="Chuck",
                        year=2004,
                        album_artists=[sum41Artist],)
        G(LibraryTrack,
            user=self.test_user,
            title="In Too Deep",
            artist=sum41Artist,
            album=chuckAlbum,
            duration=128)
        G(LibraryTrack,
            user=self.test_user,
            title="We're All To Blame",
            artist=sum41Artist,
            album=chuckAlbum,
            duration=120)
        G(LibraryTrack,
            user=self.test_user,
            title="Pieces",
            artist=sum41Artist,
            album=chuckAlbum,
            duration=125)

        response = self.get_albums()
        assert response.status_code == status.HTTP_200_OK
        albumsJsonList = response.json()[RESPONSE_KEYS.RESULTS]
        assert len(albumsJsonList) == 2