#!/usr/bin/env python
import pprint
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewRatingFileTypeMp3TestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataRatingFileTypeMp3']
    sampleDirectoryRelativePath = "test/view/track/put/rating/fileType/mp3/sample/"


    """
    null rating. There shouldn't be a rating tag in the file.
    """
    def test_trackPutRatingFileTypeMp3None(self):

        data = {
            "rating": None,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) is None


    """
    0 rating. The file's tag value should be 0.
    """
    def test_trackPutRatingFileTypeMp3Zero(self):

        data = {
            "rating": "0",
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 0


    """
    1 rating. The file's tag value should be 13.
    """
    def test_trackPutRatingFileTypeMp3One(self):

        data = {
            "rating": 1,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 13


    """
    2 rating. The file's tag value should be 1.
    """
    def test_trackPutRatingFileTypeMp3Two(self):

        data = {
            "rating": 2,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 1


    """
    3 rating. The file's tag value should be 54.
    """
    def test_trackPutRatingFileTypeMp3Three(self):

        data = {
            "rating": 3,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 54


    """
    4 rating. The file's tag value should be 64.
    """
    def test_trackPutRatingFileTypeMp3Four(self):

        data = {
            "rating": 4,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 64


    """
    5 rating. The file's tag value should be 118.
    """
    def test_trackPutRatingFileTypeMp3Five(self):

        data = {
            "rating": 5,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 118


    """
    6 rating. The file's tag value should be 128.
    """
    def test_trackPutRatingFileTypeMp3Six(self):

        data = {
            "rating": 6,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 128


    """
    7 rating. The file's tag value should be 186.
    """
    def test_trackPutRatingFileTypeMp3Seven(self):

        data = {
            "rating": 7,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 186


    """
    8 rating. The file's tag value should be 196.
    """
    def test_trackPutRatingFileTypeMp3Height(self):

        data = {
            "rating": 8,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 196


    """
    9 rating. The file's tag value should be 242.
    """
    def test_trackPutRatingFileTypeMp3Nine(self):

        data = {
            "rating": 9,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 242


    """
    10 rating. The file's tag value should be 255.
    """
    def test_trackPutRatingFileTypeMp3Ten(self):

        data = {
            "rating": 10,
        }
        response = self._loginAndPutSampleTrack(
                trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 255