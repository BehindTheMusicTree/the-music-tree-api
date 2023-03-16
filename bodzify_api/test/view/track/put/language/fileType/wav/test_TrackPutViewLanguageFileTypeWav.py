#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewLanguageFileTypeWavTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataLanguageFileTypeWav']
    sampleDirectoryRelativePath = "test/view/track/put/language/fileType/wav/sample/"


    """
    null language. There shouldn't be a language tag in the file.
    """
    def test_trackPutLanguageFileTypeWavNone(self):

        data = {
            "language": None,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE) is None


    """
    The language is updated to "Mexican".
    """
    def test_trackPutLanguageFileTypeWavMexican(self):
        data = {
            "language": "Mexican",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE) == "Mexican"
