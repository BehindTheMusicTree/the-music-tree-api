#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.album.AlbumViewTestCase import AlbumViewTestCase
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class AlbumDeleteViewTestCase1(AlbumViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewAlbumDeleteData1']
    sampleDirectoryRelativePath = "test/view/album/delete/sample/1/"

    def test_albumDelete1(self):
        self._login(self.testUser)

        """
        The album "Black Holes And Revelation" has two tracks "Assassin" and "Starlight" (with 
        respective filenames "Assassin.mp3" and "Starlight.mp3").
        The deletion of the album must delete the two tracks with their files.
        """
        response = self.delete(albumUuid="f36nS4LVDssLh4BvTSST54")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Album.objects.filter(uuid="f36nS4LVDssLh4BvTSST54").exists() == False
        assert LibraryTrack.objects.filter(user=self.testUser, title="Assassin").exists() == False
        assert LibraryTrack.objects.filter(user=self.testUser, title="Starlight").exists() == False
        assert self.doesUserTrackFileExist("Assassin.mp3") == False
        assert self.doesUserTrackFileExist("Starlight.mp3") == False
