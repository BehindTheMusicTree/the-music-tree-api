#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase11(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/11/"

    """
    - Flac file with no tag.
    - The 'title' must then be set with the file's name without the extension.
    """
    def test_libraryTrackPost11(self):
        self.login(self.testUser)

        response = self.postSampleTrack("sample_without_tags.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert LibraryTrack.objects.filter(
                user=self.testUser, title='sample_without_tags').exists()
