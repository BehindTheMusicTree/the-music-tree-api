#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCaseWav(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataWav']
    sampleDirectoryRelativePath = "test/view/track/put/sample/Wav/"

    """
    On a wav file without tags:
        - new genre "Techno";
        - new existing artist name is "Queen".
    """
    def test_trackPutWavWithoutTags(self):

        data = {
            "title": "Bohemian Raphsody",
            "artistName": "Queen",
            "albumName": "A Night At The Opera",
            "albumArtistsName": "Queen",
            "genre": "Techno",
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
