#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCaseArtist(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostDataArtist']
    sampleDirectoryRelativePath = "test/view/track/post/artist/sample/"

    """
     Existing artist "PNL"
    """
    def test_libraryTrackPostArtistExisting(self):
        self.login(self.testUser)
        response = self.postSampleTrack("1-08 - Luz De Luna.flac")
        track = LibraryTrack.objects.get(user=self.testUser, title="Luz De Luna")
        assert track.artist.name == "PNL"
