#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCase8(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataRating']

    """
    The rating 11 is above the maximum (10).
    The status code should then be 400 (bad request).
    """
    def test_trackPutRatingAboveMaximum(self):

        data = {
            "rating": 11,
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    The rating -1 is below the minimum (0).
    The status code should then be 400 (bad request).
    """
    def test_trackPutRatingBelowMinimum(self):
            
        data = {
            "rating": -1,
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    """
    The rating 5.5 is not an integer.
    The status code should then be 400 (bad request).
    """
    def test_trackPutRatingBelowMinimum(self):
            
        data = {
            "rating": 5.5,
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST