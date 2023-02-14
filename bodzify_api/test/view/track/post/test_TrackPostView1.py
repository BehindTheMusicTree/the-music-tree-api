import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCase1(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/1/"

    def test_libraryTrackPost1(self):
        self.login(self.testUser)

        """
        - FLAC
        - Non existing Album
        - One non existing Album artist
        """
        response = self.postSampleTrack("1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(user=self.testUser, title="Luz De Luna")
        assert track.artist.name == "PNL"
        assert track.album.name == "Dans La Légende"
        assert track.album.albumArtists.filter(user=self.testUser, name="PNL").exists()
        assert track.album.albumArtists.filter(user=self.testUser, name="Triste").exists()
        assert track.genre.name == "French cloud rap"
        assert track.fileExtension == ".flac"
        assert track.playlists.filter(
                user=self.testUser, name=PlaylistSpecialNames.GENRE_ALL).exists()
        assert track.playlists.filter(
                user=self.testUser, name="French cloud rap").exists()
