#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.artist.ArtistViewTestCase import ArtistViewTestCase
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDeleteViewTestCase2(ArtistViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewArtistDeleteData2']

    """
    - A track 'A Life' with artist 'Bertrand' and album 'Xavier'.
    - Album 'Xavier' has album artists 'Bertrand' and 'Coco Roùa'.
    - Deleting artist 'Bertrand' should delete:
        - track 'A Life';
        - album 'Xavier' as it has no track linked anymore;
        - artist 'Coco Roùa' as it has nor album nor track linked anymore.
    """
    def test_artistDelete2(self):
        self._login(self.testUser)
        response = self.delete(Artist.objects.get(user=self.testUser, name='Bertrand').uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LibraryTrack.objects.filter(user=self.testUser, title='A Life').exists() == False
        assert Album.objects.filter(user=self.testUser, name='Xavier').exists() == False
        assert Artist.objects.filter(user=self.testUser, name='Coco Roùa').exists() == False
