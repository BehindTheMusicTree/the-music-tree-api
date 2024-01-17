#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_NAME
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test(self):
        sum41Artist = G(Artist,
                        name="Sum 41",
                        user=self.testUser)
        chuckAlbum = G(Album, 
                        user=self.testUser,
                        name="Chuck",
                        year=2001,
                        albumArtists=[sum41Artist],)
        werealltoblameTrack = G(LibraryTrack,
                    user=self.testUser,
                    title="We're All To Blame",
                    artist=sum41Artist,
                    album=chuckAlbum,
                    duration=120)
        piecesTrack = G(LibraryTrack,
                    user=self.testUser,
                    title="Pieces",
                    artist=sum41Artist,
                    album=chuckAlbum,
                    duration=125)

        response = self.get_albums()
        assert response.status_code == status.HTTP_200_OK