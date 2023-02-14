import pytest
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase6(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/6/"

    def test_libraryTrackPost6(self):
        self.login(self.testUser)

        """
        - WAV
        - Existing artist
        - Non existing album artists
        """
        response = self.postSampleTrack("sample with tags.wav")
        assert response.status_code == 201
        track = LibraryTrack.objects.get(title="La zumba", user=self.testUser)
        assert track.artist.name == "Joni"
        assert track.album.name == "BOOM"
        assert track.album.albumArtists.filter(name="Jacky").exists()
        assert track.album.albumArtists.filter(name="Michelle").exists()
        assert track.genre.name == "j\"\"\"\"j"
        assert track.duration == 2.665374149659864
        assert track.rating == 8
        assert track.language == "French"
        assert track.fileExtension == ".wav"
        assert track.playlists.filter(name="j\"\"\"\"j").exists()
