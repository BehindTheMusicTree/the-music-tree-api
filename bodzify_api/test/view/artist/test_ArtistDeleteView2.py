#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDeleteViewTestCase2(ArtistViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewArtistDeleteData2']

    """
    - A track 'A' with artist 'B' and album 'X'.
    - Album 'X' has album artists 'B' and 'C'.
    - 'Deleting artist 'B' should delete:
        - track 'A';
        - album 'X' as it has no track linked anymore;
        - artist 'C' as it has nor album nor track linked anymore.
    """
    def test_artistDelete2(self):
        self.login(self.testUser)
        response = self.delete(Artist.objects.get(user=self.testUser, name='B').uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(user=self.testUser, title='A').exists() == False
        assert Album.objects.filter(user=self.testUser, name='X').exists() == False
        assert Artist.objects.filter(user=self.testUser, name='C').exists() == False
