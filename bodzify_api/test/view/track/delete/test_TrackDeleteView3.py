#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class TrackDeleteViewTestCase3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackDeleteData3']

    def test_libraryTrackDelete3(self):
        self.login(self.testUser)

        """
        Deleting the track '1-03 - We're All To Blame' should work even if the track has no file.
        """
        response = self._deleteTrack(trackUuid="36nS4LVDssLh4BvTARbJEK")
        assert response.status_code == status.HTTP_204_NO_CONTENT
