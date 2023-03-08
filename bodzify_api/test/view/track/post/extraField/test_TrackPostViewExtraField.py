#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseExtraField(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/extraField/sample/"

    """
     Trying to post a track with extra fields should fail with a 400 error code.
    """
    def test_libraryTrackPost1(self):
        self.login(self.testUser)
        response = self.postSampleTrack(
                "1-08 - Luz De Luna.flac", {"nonExistingField": "qofkqspofk"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
