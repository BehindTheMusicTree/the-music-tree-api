#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Album import Album


class TrackPutViewTestCase5(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData5']

    def test_libraryTrackPut5(self):

        """
        The old album shared the same name "Hello" as another one but with different artists names
        ("Kendal" for the first one and "Robert De Niro" for the second one). The new album keeps
        the same name "Hello" but puts the same artist name "Robert De Niro" as the other one.
        The old album hasn't anything linked to it anymore. It must then be deleted. 
        The track's artist is not specified. It is therefore unchanged ("Robert De Niro").
        """
        data = {
            "albumName": "Hello",
            "albumArtistsNames": "Robert De Niro",
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcSSSSSSS", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBcSSSSSSS")
        assert track.artist.name == "Robert De Niro"
        assert Album.objects.filter(name="Hello").count() == 1
