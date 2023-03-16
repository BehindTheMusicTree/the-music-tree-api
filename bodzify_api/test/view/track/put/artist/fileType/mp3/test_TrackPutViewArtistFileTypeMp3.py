#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewArtistFileTypeMp3TestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataArtistFileTypeMp3']
    sampleDirectoryRelativePath = "test/view/track/put/artist/fileType/mp3/sample/"


    """
    null artist. There shouldn't be a artist tag in the file.
    """
    def test_trackPutArtistFileTypeMp3None(self):
        data = {
            "artistName": None,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME) in [None, ""]


    """
    The artist is updated to a string of the highest length allowed.
    """
    def test_trackPutArtistFileTypeMp3LongestString(self):
        data = {
            "artistName": "a" * 100,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME) == "a" * 100
