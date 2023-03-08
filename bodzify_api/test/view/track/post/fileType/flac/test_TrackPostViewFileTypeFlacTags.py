#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseFileTypeFlacTags(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/fileType/flac/sample/"

    """
    FLAC file with all tags.
    """
    def test_trackPostFileTypeFlacTagsAll(self):
        self.login(self.testUser)

        response = self.postSampleTrack("1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Luz De Luna")
        assert track.artist.name == "PNL"
        assert track.album.name == "Dans La Légende"
        assert track.album.albumArtists.filter(user=self.testUser, name="PNL").exists()
        assert track.genre.name == "French cloud rap"
        assert track.playlists.filter(user=self.testUser, criteria__name="French cloud rap").exists()
        assert track.rating == 6
        assert track.language == "French"
        assert track.fileExtension == ".flac"
