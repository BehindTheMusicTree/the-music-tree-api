#!/usr/bin/env python
import pytest
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase6(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPostData6']
    sampleDirectoryRelativePath = "test/view/track/post/sample/6/"

    """
    - WAV file;
    - Existing artist "BOOM";
    - Non existing album artists "Jacky" and "Michelle".
    """
    def test_libraryTrackPost6(self):
        self.login(self.testUser)
        response = self.postSampleTrack("sample with tags.wav")
        assert response.status_code == 201
        track = LibraryTrack.objects.get(user=self.testUser, title="La zumba")
        assert track.artist.name == "Joni"
        assert track.album.name == "BOOM"
        assert track.album.albumArtists.filter(user=self.testUser, name="Jacky").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Michelle").exists()
        assert track.genre.name == "j\"\"\"\"j"
        assert track.duration == 2.665374149659864
        assert track.rating == 8
        assert track.language == "French"
        assert track.fileExtension == ".wav"
        assert track.playlists.filter(user=self.testUser, criteria__name="j\"\"\"\"j").exists()
