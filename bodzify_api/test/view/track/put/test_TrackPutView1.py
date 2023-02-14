#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class TrackPutViewTestCase1(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData1']
    sampleDirectoryRelativePath = "test/view/track/put/sample/1/"

    def test_libraryTrackPut1(self):

        """
        - On a mp3 file.
        - Existing artist.
        - No new album. The field albumArtistsNames is thus ignored.
        - Language not specified so unchanged.
        - Genre not specified so unchanged.
        """
        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "",
            "albumArtistsNames": "Garou",
            "rating": 200,
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Somewhere I Belong")
        assert track.artist.name == "Linkin Park"
        assert track.album_id == None
        assert track.genre.name == "Rock"
        assert track.rating == 200
        assert track.language == "Latin"
