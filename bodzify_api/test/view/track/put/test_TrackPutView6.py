#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase6(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData6']

    def test_libraryTrackPut6(self):

        """
        The old track's album A with uuid 'Lsji85mqisjdjf88MLKJY' shared the same name 'Birds' as 
        another album B with uuid 'Lsji85mqisjdjf881DJDHD' but with different artists names:
            - A album's artists are 'Joris Michel' and 'Paula Temple';
            - B album's artists are 'Joris Michel' and 'Moço'.
        The update puts artists 'Joris Michel' and 'Moço' on the track's album's artists'names. 
        Thus:
            - The 'Paula Temple' artist must be deleted as it has no track or album linked to it 
            anymore;
            - B album must be deleted for the same reason. 
        - The file is missing. The update must be proceded anyway. 
        """
        data = {
            "albumName": "Birds",
            "albumArtistsNames": "Joris Michel, Moço",
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBc48766YH", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(user=self.testUser, uuid="dyFYZTP3anyaUBc48766YH")
        print(Album.objects.filter(user=self.testUser, name='Birds').count())
        assert Album.objects.filter(user=self.testUser, name='Birds').count() == 1
        assert Album.objects.filter(
            user=self.testUser, uuid='Lsji85mqisjdjf88MLKJY').exists() == False
        assert Artist.objects.filter(name='Paula Temple').exists() == False
