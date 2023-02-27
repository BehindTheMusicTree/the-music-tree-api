#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCase1(TrackViewTestCase):

        fixtures = ['initial_data', 'TestUserData']
        sampleDirectoryRelativePath = "test/view/track/post/sample/FileError/"

        """
        The request should fail with 400 (bad request) because the file is missing.
        """
        def test_libraryTrackPostFileErrorMissing(self):
                self.login(self.testUser)
                response = self.postSampleTrack()
                assert response.status_code == status.HTTP_400_BAD_REQUEST

        """
        The extension of the file sent (jpeg) should not be allowed with 
        response 400 (bad request).
        """
        def test_libraryTrackPostFileErrorBadExtensionJpeg(self):
                self.login(self.testUser)
                response = self.postSampleTrack("image.jpeg")
                assert response.status_code == status.HTTP_400_BAD_REQUEST

        """
        The extension of the file sent (mp4) should not be allowed with 
        response 400 (bad request).
        """
        def test_libraryTrackPostFileErrorBadExtensionMp4(self):
                self.login(self.testUser)
                response = self.postSampleTrack("bad_extension.mp4")
                assert response.status_code == status.HTTP_400_BAD_REQUEST
                