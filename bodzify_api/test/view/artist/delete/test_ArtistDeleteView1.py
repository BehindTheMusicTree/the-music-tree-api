#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDeleteViewTestCase1(ArtistViewTestCase):

    """
        Artist "Muse" with one track "Assassin".
    """
    def test_artistDeleteWithOneTrack(self):
        museArtist = G(Artist, name="Muse", user=self.testUser)
        assassinTrack = G(
            LibraryTrack,
            user=self.testUser,
            title="Assassin",
            artist=museArtist,
            genre=self.testUserGenrelessGenre,
            duration=0)

        response = self._loginAndDelete(artistUuid=museArtist.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Artist.objects.filter(uuid=museArtist.uuid).exists() == False
        assert LibraryTrack.objects.filter(uuid=assassinTrack.uuid).exists() == False
