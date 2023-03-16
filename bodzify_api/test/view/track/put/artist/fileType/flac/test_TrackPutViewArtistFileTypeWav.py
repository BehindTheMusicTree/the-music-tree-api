#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewArtistFileTypeFlacTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataArtistFileTypeFlac']
    sampleDirectoryRelativePath = "test/view/track/put/artist/fileType/flac/sample/"


    """
    null artist. There shouldn't be a artist tag in the file.
    """
    def test_trackPutArtistFileTypeFlacNone(self):
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
    def test_trackPutArtistFileTypeFlacLongestString(self):
        data = {
            "artistName": "a" * 100,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME) == "a" * 100
