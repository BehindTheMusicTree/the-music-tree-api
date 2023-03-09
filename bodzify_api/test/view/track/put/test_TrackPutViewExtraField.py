#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackPutViewTestCaseExtraField(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataExtraField']

    """
    Trying to post a track with extra fields should fail with a 400 error code.
    """
    def test_trackPutExtraField(self):

        data = {
            "title": "Somewhere I Belong",
            "nonExistingField": "oifjqoif",
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
