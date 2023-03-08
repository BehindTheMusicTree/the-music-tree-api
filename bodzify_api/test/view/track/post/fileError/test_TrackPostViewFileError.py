#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase1(TrackViewTestCase):

        fixtures = ['initial_data', 'TestUserData']
        sampleDirectoryRelativePath = "test/view/track/post/fileError/sample/"

        """
        The request should fail with 400 (bad request) because the file is missing.
        """
        def test_libraryTrackPostFileErrorMissing(self):
                response = self._loginAndPostSampleTrack()
                assert response.status_code == status.HTTP_400_BAD_REQUEST

        """
        The extension of the file sent (jpeg) should not be allowed with 
        response 400 (bad request).
        """
        def test_libraryTrackPostFileErrorBadExtensionJpeg(self):
                response = self._loginAndPostSampleTrack("image.jpeg")
                assert response.status_code == status.HTTP_400_BAD_REQUEST

        """
        The extension of the file sent (mp4) should not be allowed with 
        response 400 (bad request).
        """
        def test_libraryTrackPostFileErrorBadExtensionMp4(self):
                response = self._loginAndPostSampleTrack("bad_extension.mp4")
                assert response.status_code == status.HTTP_400_BAD_REQUEST
                