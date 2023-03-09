#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseFileTagsWav(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostDataFileTypeWavTags']
    sampleDirectoryRelativePath = "test/view/track/post/sample/fileType/wav/sample/"

    """
    - Wav file with all tags;
    - Existing artist "BOOM";
    - Non existing album artists "Jacky" and "Michelle".
    """
    def test_trackPostFileTypeWavTagsAll(self):
        response = self._loginAndPostSampleTrack("sample with tags.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == "Joni"
        assert self.savedTrack.album.name == "BOOM"
        assert self.savedTrack.album.albumArtists.filter(
                user=self.testUser, name="Jacky").exists()
        assert self.savedTrack.album.albumArtists.filter(
                user=self.testUser, name="Michelle").exists()
        assert self.savedTrack.genre.name == "j\"\"\"\"j"
        assert self.savedTrack.duration == 2.665374149659864
        assert self.savedTrack.rating == 8
        assert self.savedTrack.language == "French"
        assert self.savedTrack.fileExtension == ".wav"
        assert self.savedTrack.playlists.filter(
                user=self.testUser, criteria__name="j\"\"\"\"j").exists()


    """
    - Wav file with no tag.
    """
    def test_trackPostFileTypeWavTagsNone(self):
        response = self._loginAndPostSampleTrack("sample_without_tags.wav")
        assert response.status_code == status.HTTP_201_CREATED