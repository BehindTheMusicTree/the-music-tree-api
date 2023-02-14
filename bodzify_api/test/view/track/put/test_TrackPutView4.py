#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackPutViewTestCase4(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData4']
    sampleDirectoryRelativePath = "test/view/track/put/sample/4/"

    def test_libraryTrackPut4(self):

        """
        - title not specified so unchanged.
        - Max rating.
        - Weird language.
        - albumName not specified so unchanged. Thus the albumArtistsNames field is ignored.
        """
        data = {
            "artistName": "",
            "albumArtistsNames": "Queen",
            "genre": "Lsjdqoiqsicqjsof8800",
            "rating": 255,
            "language": "French12ééù12"
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcLDDDDDS", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBcLDDDDDS")
        assert track.title == "Test4 - Track"
        assert track.language == "French12ééù12"
        assert track.rating == 255
        assert track.album.name == "Test4 - Album"
