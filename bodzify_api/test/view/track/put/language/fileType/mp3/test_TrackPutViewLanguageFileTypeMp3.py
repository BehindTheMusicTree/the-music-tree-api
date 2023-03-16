#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewLanguageFileTypeMp3TestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataLanguageFileTypeMp3']
    sampleDirectoryRelativePath = "test/view/track/put/language/fileType/mp3/sample/"


    """
    null language. There shouldn't be a language tag in the file.
    """
    def test_trackPutLanguageFileTypeMp3None(self):
        data = {
            "language": None,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE) in [None, ""]


    """
    The language is updated to a string of the highest length allowed.
    """
    def test_trackPutLanguageFileTypeMp3LongestString(self):
        data = {
            "language": "a" * 100,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE) == "a" * 100
