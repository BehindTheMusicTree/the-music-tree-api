#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseAlbum(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostDataAlbum']
    sampleDirectoryRelativePath = "test/view/track/post/album/sample/"

    """
     - non existing album "Dans La Légende";
     - one non existing Album artist "Triste" and one existing "PNL";
    """
    def test_libraryTrackPostAlbumNonExisting(self):
        response = self._loginAndPostSampleTrack("1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.name == "Dans La Légende"
        assert self.savedTrack.album.albumArtists.filter(user=self.testUser, name="PNL").exists()
        assert self.savedTrack.album.albumArtists.filter(
                user=self.testUser, name="Triste").exists()
