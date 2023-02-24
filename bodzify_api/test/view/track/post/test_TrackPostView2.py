#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase2(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/2/"

    """
    - No rating. The resulting rating must be 0.
    - FLAC
    """
    def test_libraryTrackPost2(self):
        self.login(self.testUser)

        response = self.postSampleTrack("sample_without_rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Je suis sympa")
        assert track.rating == 0
