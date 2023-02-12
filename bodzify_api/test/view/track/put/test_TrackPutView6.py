from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase6(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData6']

    def test_libraryTrackPut6(self):
        self.login(self.testUser)

        """
        - The old track's album '1' shared the same name as another one '2' but with different 
        artists names:
            - '1' album's artists are 'A' and 'B';
            - '2' album's artists are 'A' and 'C'.
        The update puts artists 'A' and 'C' on the artists'names of the track's album. Thus:
            - Artist B must be deleted as it has no track linked anymore;
            - Album '1' must be deleted for the same reason. 
        - The file is missing. The update must be proceded anyway. 
        """
        data = {
            "albumName": "Test6 - Album",
            "albumArtistsNames": "Test6 - Artist1, Test6 - Artist2",
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBc48766YH", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBc48766YH")
        assert Album.objects.filter(name='Test6 - Album').count() == 1
        assert Album.objects.filter(uuid='Lsji85mqisjdjf88MLKJY').exists() == False
        assert Artist.objects.filter(name='Test6 - Artist3').exists() == False
