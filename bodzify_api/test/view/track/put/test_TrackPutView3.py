#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData3']
    sampleDirectoryRelativePath = "test/view/track/put/sample/3/"

    def test_libraryTrackPut3(self):

        """
        Update:
         - on a wav file entitled "La Zumba";
         - the former artist "Joni", not having any track related left, must be deleted;
         - the new artist specified is empty so no artist;
         - same album's name "American Idiot" as an existing one but with an album 
         artist named "Queen". Thus a new album has to be created;
         - the old album "American Idiot" (with no album artists) still has a track linked to it. 
         It must therefore not be 
         deleted. We should then have two albums "American Idiot" (one with no album artist, one 
         with album artist "Queen")
         - rating isn't specified so unchanged (255);
         - the previous track's album "BOOM" hasn't anythink linked to it anymore. It must then be 
        deleted;
         - new genre "Nu metal".
        """
        data = {
            "title": "Bohemian Raphsody",
            "artistName": "",
            "albumName": "American Idiot",
            "albumArtistsNames": "Queen",
            "genre": "L1ZG85munGytJb885WWJN8",
            "language": "French"
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcLYVHJ3A", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Bohemian Raphsody")
        assert track.artist_id == None
        assert track.album.name == "American Idiot"
        assert track.album.albumArtists.filter(name="Queen").exists()
        assert Album.objects.filter(user=self.testUser, name="American Idiot").count() == 2
        assert Album.objects.filter(user=self.testUser, name="BOOM").exists() == False
        assert track.genre.name == "Nu metal"
        assert track.rating == 255
        assert track.language == "French"
        assert Artist.objects.filter(name="Joni").count() == 0
