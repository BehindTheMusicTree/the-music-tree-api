#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCaseArtist(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostDataArtist']
    sampleDirectoryRelativePath = "test/view/track/post/artist/sample/"

    """
    Existing artist "PNL"
    """
    def test_libraryTrackPostArtistExisting(self):
        self._loginAndPostSampleTrack("1-08 - Luz De Luna.flac")
        assert self.postedTrack.artist.name == "PNL"
