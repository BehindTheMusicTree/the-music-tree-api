#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase8(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/8/"

    """
    Wrong extension (mp4)
    """
    def test_libraryTrackPost8(self):
        self.login(self.testUser)
        response = self.postSampleTrack("bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
