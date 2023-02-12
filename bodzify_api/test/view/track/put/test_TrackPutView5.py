#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Album import Album


class TrackPutViewTestCase5(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData5']

    def test_libraryTrackPut5(self):
        self.login(self.testUser)

        """
        - The old album shared the same name as an other one but with different artists names.
        The new album keeps the same name but puts the same artists names as the other one.
        - artist not specified so unchanged.
        """
        data = {
            "albumName": "Test5 - Album",
            "albumArtistsNames": "Test5 - Artist2",
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcSSSSSSS", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBcSSSSSSS")
        assert track.artist.name == "Test5 - Artist2"
        assert Album.objects.filter(name="Test5 - Album").count() == 1
