#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseFileTypeFlacTags(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/fileType/flac/sample/"


    """
    FLAC file with all tags.
    """
    def test_trackPostFileTypeFlacTagsAll(self):
        response = self._loginAndPostSampleTrack("1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.postedTrack.artist.name == "PNL"
        assert self.postedTrack.album.name == "Dans La Légende"
        assert self.postedTrack.album.albumArtists.filter(user=self.testUser, name="PNL").exists()
        assert self.postedTrack.genre.name == "French cloud rap"
        assert self.postedTrack.playlists.filter(user=self.testUser, criteria__name="French cloud rap").exists()
        assert self.postedTrack.rating == 6
        assert self.postedTrack.language == "French"
        assert self.postedTrack.fileExtension == ".flac"


    """
    - Flac file with no tag.
    - The 'title' must then be set with the file's name without the extension.
    """
    def test_libraryTrackPost11(self):
        response = self._loginAndPostSampleTrack("sample_without_tags.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.postedTrack.exists()
