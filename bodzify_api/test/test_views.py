import os

from django.urls import reverse
from django.test import TestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames
from bodzify_api.model.criteria.Criteria import Criteria
import bodzify_api.settings as settings

USER_TEST_PK = 2

class ViewTestCase(TestCase):

    fixtures = ['initial_data', 'test_data']

    def test_login(self):
        client = Client()
        data = {
            "username": "user_test", 
            "password": "user_test"
        }
        response = client.post(
            reverse("token-obtain-pair"),
            data
        )
        assert response.status_code == 200

        return response.access

    def postFile(self, file, client, postExtra):
        client.post(
                path='/tracks/', 
                data={'file': file}, 
                extra=postExtra)


    def test_libraryTrackPost(self):
        userTest = User.objects.get(pk=USER_TEST_PK)
        client = Client()

        token = self.test_login()
        postExtra={'HTTP_AUTHORIZATION': f'Bearer {token}'}

        currentFolder = os.path.dirname(__file__)

        tooBigSampleTrackRelativePath = settings.TEST_SAMPLE_PATH + "29Mo.flac"
        badExtensionSampleTrackRelativePath = settings.TEST_SAMPLE_PATH + "bad_extension.mp4"
        sampleTrackWithNonExistingGenreFooRelativePath = (
            settings.TEST_SAMPLE_PATH + "genre_non_existing.mp3")
        goodFlacSampleRelativePath = settings.TEST_SAMPLE_PATH + "1-08 - Luz De Luna.flac"
        goodWavSampleRelativePath = settings.TEST_SAMPLE_PATH + "sample.wav"
        goodMp3SampleRelativePath = settings.TEST_SAMPLE_PATH + "Eminem_Without_Me_sans_genre.mp3"
        withAllTagsSampleRelativePath = settings.TEST_SAMPLE_PATH + "with_all_tags.mp3"

        tooBigSampleTrackAbsolutePath = os.path.join(currentFolder, 
            tooBigSampleTrackRelativePath)
        badExtensionSampleTrackAbsolutePath = os.path.join(currentFolder, 
            badExtensionSampleTrackRelativePath)
        sampleTrackWithNonExistingGenreFooAbsolutePath = os.path.join(currentFolder, 
            sampleTrackWithNonExistingGenreFooRelativePath)
        goodFlacSampleAbsolutePath = os.path.join(currentFolder, goodFlacSampleRelativePath)
        goodWavSampleAbsolutePath = os.path.join(currentFolder, goodWavSampleRelativePath)
        goodMp3SampleAbsolutePath = os.path.join(currentFolder, goodMp3SampleRelativePath)
        withAllTagsSampleAbsolutePath = os.path.join(currentFolder, withAllTagsSampleRelativePath)
        
        with open(tooBigSampleTrackAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 400
        
        with open(badExtensionSampleTrackAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 400
        
        with open(sampleTrackWithNonExistingGenreFooAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 201
        assert Criteria.objects.filter(user=userTest, type__name="Foo").exists()
        
        with open(goodFlacSampleAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 201
        track = LibraryTrack.objects.get(__path__endswith="1-08 - Luz De Luna.flac", user=userTest)
        assert track.title == "Luz De Luna"
        assert track.artist == "PNL"
        assert track.album == "Dans La Légende"
        assert track.genre == "French cloud rap"
        assert track.fileExtension == ".flac"

        assert Playlist.objects.get(
            user=userTest,
            name="French cloud rap"
        ) in track.playlists
        
        with open(goodWavSampleAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 201
        track = LibraryTrack.objects.get(__path__endswith="sample.wav", user=userTest)
        assert track.title == "La zumba"
        assert track.artist == "Joni"
        assert track.album == "BOOM"
        assert track.genre == "j\"\"\"j"
        assert track.duration == "2.665374149659864"
        assert track.rating == 10
        assert track.language == "French"
        assert track.fileExtension == ".wav"

        assert Playlist.objects.get(
            user=userTest,
            name="French cloud rap"
        ) in track.playlists


        with open(withAllTagsSampleAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 201
        
        with open(goodMp3SampleAbsolutePath) as file:
            response = self.postFile(file, client, postExtra)
        assert response.status_code == 201

        track = LibraryTrack.objects.get(
            __path__endswith="Eminem_Without_Me_sans_genre.mp3",
            user=userTest)
        assert track.title == "Without Me"
        assert track.artist == "Eminem"
        assert track.album == "The Eminem Show (Expanded Edition)"
        assert track.genre == "Genreless"
        assert track.fileExtension == ".mp3"

        assert Playlist.objects.get(
            user=userTest,
            name=PlaylistSpecialNames.GENRE_ALL
        ) in track.playlists

        assert Playlist.objects.get(
            user=userTest,
            name=PlaylistSpecialNames.GENRE_GENRELESS
        ) in track.playlists
