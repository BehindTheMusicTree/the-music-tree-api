#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist


class AlbumDeleteViewTestCase2(AlbumViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewAlbumDeleteData2']

    def test_albumDelete2(self):
        self._login(self.testUser)

        """
        The album "Black Holes And Revelation" has:
         - one track "Assassin" with artist "Matthew Bellamy";
         - two album artists named "Muse" and "Feat".
        The artist "Feat" has another track linked to it but in another album. 
        This test checks if the album deletion:
         - triggers the deletion of the artist "Matthew Bellamy" as it was not linked to any album and
         the only track it was linked to is deleted;
         - triggers the deletion of the artist "Muse" as it was not linked to any track and
         the only album it was linked to is deleted;
         - does not trigger the deletion of the artist "Feat" as it has still a track linked to it.
        """
        response = self.delete(albumUuid="f36nS4LVDssLh4BvTSST54")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(user=self.testUser, name="Matthew Bellamy").exists() == False
        assert Artist.objects.filter(user=self.testUser, name="Muse").exists() == False
        assert Artist.objects.filter(user=self.testUser, name="Feat").exists() == True
