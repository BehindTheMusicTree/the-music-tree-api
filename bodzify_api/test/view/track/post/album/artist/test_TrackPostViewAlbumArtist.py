#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseAlbumArtist(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/album/artist/sample/"

    """
    - Non existing album artists "Jacky" and "Michelle".
    """
    def test_trackPostAlbumArtistNonExisting(self):
        self._loginAndPostSampleTrack("sample with tags.wav")
        assert self.postedTrack.album.albumArtists.count() == 2
        assert self.postedTrack.album.albumArtists.filter(
                user=self.testUser, name="Jacky").exists()
        assert self.postedTrack.album.albumArtists.filter(
                user=self.testUser, name="Michelle").exists()
