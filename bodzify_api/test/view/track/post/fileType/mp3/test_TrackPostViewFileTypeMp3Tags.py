#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseFileTypeMp3Tags(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/fileType/mp3/sample/"

    """
    - Mp3 with all tags;
    - the rating source is MusicBee with 2 starts.
    """
    def test_trackPostFileTypeMp3TagsAll(self):
        response = self._loginAndPostSampleTrack("with_all_tags.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.postedTrack.artist.name == "2Be3"
        assert self.postedTrack.album.name == "Demain"
        assert self.postedTrack.album.albumArtists.filter(user=self.testUser, name="2Be3").exists()
        assert self.postedTrack.album.albumArtists.filter(user=self.testUser, name="Fillip").exists()
        assert self.postedTrack.genre.name == "Boys band eurodance"
        assert self.postedTrack.playlists.filter(user=self.testUser, criteria__name="Boys band eurodance").exists()
        assert self.postedTrack.rating == 4
        assert self.postedTrack.language == "French"
        assert self.postedTrack.fileExtension == ".mp3"

