from rest_framework import status

from bodzify_api.test.view.track.library.LibraryTrackViewTestCase import LibraryTrackViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames


class LibraryTrackPostViewTestCase(LibraryTrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackLibraryPostData']

    def setUp(self) -> None:
        return super().setUp(sampleRelativePath="test/view/track/library/post/sample/")

    def test_libraryTrackPost(self):
        self.login(self.testUser)

        response = self.postSampleTrack("post_image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = self.postSampleTrack(
            "post_Big_File 1-01 - Shine On You Crazy Diamond, Parts I–V.flac")
        assert response.status_code == status.HTTP_201_CREATED

        response = self.postSampleTrack("post_sample_without_rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="Je suis sympa", user=self.testUser)
        assert track.rating == 0

        response = self.postSampleTrack("post_bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = self.postSampleTrack("post_genre_foo_non_existing.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert Criteria.objects.filter(user=self.testUser, name="Foo").exists()

        response = self.postSampleTrack("post_1-08 - Luz De Luna.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="Luz De Luna", user=self.testUser)
        assert track.artist == "PNL"
        assert track.album == "Dans La Légende"
        assert track.genre.name == "French cloud rap"
        assert track.fileExtension == ".flac"

        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_ALL).exists()
        assert track.playlists.filter(name="French cloud rap").exists()

        response = self.postSampleTrack("post_sample.wav")
        assert response.status_code == 201
        track = LibraryTrack.objects.get(title="La zumba", user=self.testUser)
        assert track.artist == "Joni"
        assert track.album == "BOOM"
        assert track.genre.name == "j\"\"\"\"j"
        assert track.duration == "2.665374149659864"
        assert track.rating == 8
        assert track.language == "French"
        assert track.fileExtension == ".wav"

        assert track.playlists.filter(name="j\"\"\"\"j").exists()

        response = self.postSampleTrack("post_with_all_tags.mp3")
        assert response.status_code == status.HTTP_201_CREATED

        response = self.postSampleTrack("post_Eminem_Without_Me_sans_genre.mp3")
        assert response.status_code == status.HTTP_201_CREATED

        track = LibraryTrack.objects.get(title="Without Me", user=self.testUser)
        assert track.artist == "Eminem"
        assert track.album == "The Eminem Show (Expanded Edition)"
        assert track.genre.name == "Genreless"
        assert track.fileExtension == ".mp3"
        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_GENRELESS).exists()
        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_ALL).exists()
