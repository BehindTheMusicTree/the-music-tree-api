#!/usr/bin/env python
import pprint
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseMp3(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/mp3/sample/"

    """
    - mp3 
    - With all tags
    """
    def test_libraryTrackPostMp3WithAllTags(self):
        self.login(self.testUser)
        response = self.postSampleTrack("with_all_tags.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        # TODO: test all file tags
