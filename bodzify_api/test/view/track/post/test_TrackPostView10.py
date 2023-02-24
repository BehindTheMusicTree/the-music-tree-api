#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase10(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/10/"

    """
    - Wav file with no tag.
    """
    def test_libraryTrackPost10(self):
        self.login(self.testUser)

        response = self.postSampleTrack("sample_without_tags.wav")
        assert response.status_code == status.HTTP_201_CREATED
