#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewRatingFileTypeFlacTestCase(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataRatingFileTypeFlac']
    sampleDirectoryRelativePath = "test/view/track/put/rating/fileType/flac/sample/"


    """
    null rating. There shouldn't be a rating tag in the file.
    """
    def test_trackPutRatingFileTypeFlacNone(self):

        data = {
            "rating": None,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) is None


    """
    0 rating. The file's tag value should be 0.
    """
    def test_trackPutRatingFileTypeFlacZero(self):

        data = {
            "rating": "0",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 0


    """
    1 rating. The file's tag value should be 10.
    """
    def test_trackPutRatingFileTypeFlacOne(self):

        data = {
            "rating": 1,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 10


    """
    2 rating. The file's tag value should be 20.
    """
    def test_trackPutRatingFileTypeFlacTwo(self):

        data = {
            "rating": 2,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 20


    """
    3 rating. The file's tag value should be 30.
    """
    def test_trackPutRatingFileTypeFlacThree(self):

        data = {
            "rating": 3,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 30


    """
    4 rating. The file's tag value should be 40.
    """
    def test_trackPutRatingFileTypeFlacFour(self):

        data = {
            "rating": 4,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 40


    """
    5 rating. The file's tag value should be 50.
    """
    def test_trackPutRatingFileTypeFlacFive(self):

        data = {
            "rating": 5,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 50


    """
    6 rating. The file's tag value should be 60.
    """
    def test_trackPutRatingFileTypeFlacSix(self):

        data = {
            "rating": 6,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 60


    """
    7 rating. The file's tag value should be 70.
    """
    def test_trackPutRatingFileTypeFlacSeven(self):

        data = {
            "rating": 7,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 70


    """
    8 rating. The file's tag value should be 80.
    """
    def test_trackPutRatingFileTypeFlacHeight(self):

        data = {
            "rating": 8,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 80


    """
    9 rating. The file's tag value should be 90.
    """
    def test_trackPutRatingFileTypeFlacNine(self):

        data = {
            "rating": 9,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 90


    """
    10 rating. The file's tag value should be 100.
    """
    def test_trackPutRatingFileTypeFlacTen(self):

        data = {
            "rating": 10,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, AudioMetadataService.METADATA_DICT_KEYS.RATING) == 100
    