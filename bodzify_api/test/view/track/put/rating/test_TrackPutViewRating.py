#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCase8(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataRating']

    """
    Rating isn't specified. It must not be updated.
    """
    def test_trackPutRatingUnchanged(self):

        data = {
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == 2
        

    """
    Updating the rating value to 0
    """
    def test_trackPutRatingZero(self):

        data = {
            "rating": 0
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == 0
        

    """
    Updating the rating value to 4
    """
    def test_trackPutRatingFour(self):

        data = {
            "rating": 4
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == 4
        

    """
    Updating the rating value to 10
    """
    def test_trackPutRatingTen(self):

        data = {
            "rating": 10
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == 10
        

    """
    Rating value is empty. The updated value must be None.
    """
    def test_trackPutRatingNone(self):

        data = {
            "rating": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTADDDDD", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == None


    """
    The rating 11 is above the maximum (10).
    The status code should then be 400 (bad request).
    """
    def test_trackPutRatingAboveMaximum(self):

        data = {
            "rating": 11,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    The rating -1 is below the minimum (0).
    The status code should then be 400 (bad request).
    """
    def test_trackPutRatingBelowMinimum(self):
            
        data = {
            "rating": -1,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    The rating 5.5 is not an integer.
    The status code should then be 400 (bad request).
    """
    def test_trackPutRatingBelowMinimum(self):
            
        data = {
            "rating": 5.5,
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    