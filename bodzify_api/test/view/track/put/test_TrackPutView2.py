#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase2(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData2']
    sampleDirectoryRelativePath = "test/view/track/put/sample/2/"

    def test_trackPut2(self):

        """
        - On a FLAC file with uuid "36nS4LVDoihoihvTARbJEK";
        - Non existing new artist "Green Day";
        - Old track didn't have an album;
        - Lowest rating 0;
        - An album artist "Green Day" is sent twice. Only one must be created;
        - A space lies at the end of the album's artists' names. It musn't be taken into account.
        - New existing genre "Rock".
        """
        data = {
            "title": "Give Me Novocain",
            "artistName": "Green Day",
            "albumName": "American Idiot",
            "albumArtistsName": "Green Day, RATM, Green Day, ",
            "genreName": "Rock",  
            "rating": 0,
            "language": "English, German"
        }
        response = self._putSampleTrack(trackUuid="36nS4LVDoihoihvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Give Me Novocain")
        assert track.artist.name == "Green Day"
        assert track.album.name == "American Idiot"
        assert track.album.albumArtists.count() == 2
        assert track.album.albumArtists.filter(name="Green Day").exists()
        assert Artist.objects.filter(name="Green Day").count() == 1
        assert track.genre.name == "Rock"
        assert track.rating == 0
        assert track.language == "English, German"
