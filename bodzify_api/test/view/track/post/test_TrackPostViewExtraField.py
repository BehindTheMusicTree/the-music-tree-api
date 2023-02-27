#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCaseExtraField(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
     Trying to post a track with extra fields should fail with a 400 error code.
    """
    def test_libraryTrackPost1(self):
        self.login(self.testUser)
        response = self.postSampleTrack(
                "1-08 - Luz De Luna.flac", {"nonExistingField": "qofkqspofk"})
        assert response == status.HTTP_400_BAD_REQUEST
