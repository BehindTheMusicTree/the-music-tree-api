#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewAlbumFileTypeFlacTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbumFileTypeFlac']
    sampleDirectoryRelativePath = "test/view/track/put/album/fileType/flac/sample/"


    """
    null album. There shouldn't be a album tag in the file.
    """
    def test_trackPutAlbumFileTypeFlacNone(self):
        data = {
            "albumName": None,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME) in [None, ""]


    """
    The album is updated to a string of the highest length allowed.
    """
    def test_trackPutAlbumFileTypeFlacLongestString(self):
        data = {
            "albumName": "a" * 100,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME) == "a" * 100
