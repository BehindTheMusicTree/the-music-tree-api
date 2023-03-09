#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackPutViewTestCase1(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData1']
    sampleDirectoryRelativePath = "test/view/track/put/sample/1/"

    """
    - On a mp3 file.
    - Existing artist.
    - No new album. The field albumArtistsName is thus ignored.
    - Language not specified so unchanged.
    - Genre "Genreless" not specified so unchanged.
    """
    def test_trackPut1(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "",
            "albumArtistsName": "Garou",
            "rating": 200,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(title="Somewhere I Belong")
        assert track.artist.name == "Linkin Park"
        assert track.album_id == None
        assert track.genre.name == "Genreless"
        assert track.rating == 200
        assert track.language == "Latin"
