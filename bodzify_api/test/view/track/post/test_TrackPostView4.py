import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCase4(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/4/"

    def test_libraryTrackPost4(self):
        self.login(self.testUser)

        """
        - Without genre.
        - With two album artists.
        - One album artist existing.
        - No artist.
        """
        response = self.postSampleTrack("Eminem_Without_Me_sans_genre.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="Without Me", user=self.testUser)
        assert track.artist_id is None
        assert track.album.name == "The Eminem Show (Expanded Edition)"
        assert track.genre.name == "Genreless"
        assert track.fileExtension == ".mp3"
        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_GENRELESS).exists()
        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_ALL).exists()
        assert track.album.albumArtists.filter(name="Eminem").exists()
        assert track.album.albumArtists.filter(name="Dad").exists()
