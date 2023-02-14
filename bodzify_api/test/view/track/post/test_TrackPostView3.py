import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames


@pytest.mark.django_db
class TrackPostViewTestCase3(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/3/"

    def test_libraryTrackPost3(self):
        self.login(self.testUser)

        # Wrong extension(jpeg)
        response = self.postSampleTrack("post_image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        """
        As the file is too big to be uploaded on Github, the pytest won't work during Github's
        actions. Therefore we have to comment this test before any dev push (as it triggers 
        Github actions)
        
        response = self.postSampleTrack(
            "post_Big_File 1-01 - Shine On You Crazy Diamond, Parts I–V.flac")
        assert response.status_code == status.HTTP_201_CREATED
        """

        """
        - No rating
        - FLAC
        """
        response = self.postSampleTrack("sample_without_rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="Je suis sympa", user=self.testUser)
        assert track.rating == 0

        # Wrong extension (mp4)
        response = self.postSampleTrack("post_bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Genre non existing
        response = self.postSampleTrack("post_genre_foo_non_existing.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert Criteria.objects.filter(user=self.testUser, name="Foo").exists()

        # WAV
        # Existing artist
        # Non existing album artists
        response = self.postSampleTrack("post_sample.wav")
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

        # With all tags.
        response = self.postSampleTrack("post_with_all_tags.mp3")
        assert response.status_code == status.HTTP_201_CREATED

        # Without genre.
        response = self.postSampleTrack("post_Eminem_Without_Me_sans_genre.mp3")
        assert response.status_code == status.HTTP_201_CREATED

        # With two album artists.
        # One album artist existing.
        # No artist.
        track = LibraryTrack.objects.get(title="Without Me", user=self.testUser)
        assert track.artist_id is None
        assert track.album.name == "The Eminem Show (Expanded Edition)"
        assert track.genre.name == "Genreless"
        assert track.fileExtension == ".mp3"
        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_GENRELESS).exists()
        assert track.playlists.filter(name=PlaylistSpecialNames.GENRE_ALL).exists()
        assert track.album.albumArtists.filter(name="Eminem").exists()
        assert track.album.albumArtists.filter(name="Dad").exists()
