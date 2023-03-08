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
        assert self.postedTrack.artist.name == "Joni"
        assert self.postedTrack.album.name == "BOOM"
        assert self.postedTrack.album.albumArtists.filter(
                user=self.testUser, name="Jacky").exists()
        assert self.postedTrack.album.albumArtists.filter(
                user=self.testUser, name="Michelle").exists()
        assert self.postedTrack.genre.name == "j\"\"\"\"j"
        assert self.postedTrack.duration == 2.665374149659864
        assert self.postedTrack.rating == 8
        assert self.postedTrack.language == "French"
        assert self.postedTrack.fileExtension == ".wav"
        assert self.postedTrack.playlists.filter(
                user=self.testUser, criteria__name="j\"\"\"\"j").exists()


    """
    - Wav file with no tag.
    """
    def test_trackPostFileTypeWavTagsNone(self):
        response = self._loginAndPostSampleTrack("sample_without_tags.wav")
        assert response.status_code == status.HTTP_201_CREATED