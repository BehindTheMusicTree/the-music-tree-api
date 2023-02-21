#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/3/"

    """
    Wrong extension(jpeg).
    """
    def test_libraryTrackPost3(self):
        self.login(self.testUser)
        response = self.postSampleTrack("image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
