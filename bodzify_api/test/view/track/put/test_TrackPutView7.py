#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase7(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData7']
    sampleDirectoryRelativePath = "test/view/track/put/sample/7/"

    def test_libraryTrackPut7(self):

        """
         - on a wav file without tags;
         - new genre "Techno";
         - new artist name is "Queen".
        """
        data = {
            "title": "Bohemian Raphsody",
            "artistName": "Queen",
            "albumName": "A Night At The Opera",
            "albumArtistsNames": "Queen",
            "genre": "L1ZG85munGytJb885WWJN8",
            "language": "French"
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcLYVHJ3A", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Bohemian Raphsody")
        assert track.artist.name == "Queen"
        assert track.album.name == "A Night At The Opera"
        assert track.album.albumArtists.filter(name="Queen").exists()
        assert track.rating == 8
        assert track.language == "French"
        assert Artist.objects.filter(name="Joni").count() == 0
