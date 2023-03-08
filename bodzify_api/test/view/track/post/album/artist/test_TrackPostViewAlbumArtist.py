#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase6(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/6/"

    """
    - Non existing album artists "Jacky" and "Michelle".
    """
    def test_libraryTrackPostAlbumArtistNonExisting(self):
        self.login(self.testUser)
        response = self.postSampleTrack("sample with tags.wav")
        track = LibraryTrack.objects.get(user=self.testUser, title="La zumba")
        assert track.album.albumArtists.count() == 2
        assert track.album.albumArtists.filter(user=self.testUser, name="Jacky").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Michelle").exists()
