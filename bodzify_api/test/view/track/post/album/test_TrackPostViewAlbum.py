#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseAlbum(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostDataAlbum']
    sampleDirectoryRelativePath = "test/view/track/post/album/sample/"

    """
     - non existing album "Dans La Légende";
     - one non existing Album artist "Triste" and one existing "PNL";
    """
    def test_libraryTrackPostAlbumNonExisting(self):
        self.login(self.testUser)
        response = self.postSampleTrack("1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Luz De Luna")
        assert track.album.name == "Dans La Légende"
        assert track.album.albumArtists.filter(user=self.testUser, name="PNL").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Triste").exists()
