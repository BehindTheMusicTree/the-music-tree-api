import os
import json
import magic

from rest_framework import status

from django.urls import reverse
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames
from bodzify_api.model.criteria.Criteria import Criteria
import bodzify_api.settings as settings

USER_TEST_PK = 2

class ViewTestCase(TestCase):

    fixtures = ['initial_data', 'test_data']

    def setUp(self) -> None:
        self.mime = magic.Magic(mime=True)
        self.client = Client()
        return super().setUp()

    def test_login(self):
        client = Client()
        data = {
            "username": "user_test", 
            "password": "user_test"
        }
        response = client.post(reverse("token-obtain-pair"), data)

        assert response.status_code == status.HTTP_200_OK
        return json.loads(response.content)['access']


    def postTrackFile(self, filePath, postExtra):
        trackFile = SimpleUploadedFile(
            name=filePath,
            content=b"file_content",
            content_type=self.mime.from_file(filePath)
        )
        print(trackFile)
        return self.client.post(
            path=reverse('librarytrack-list'), data={'file': trackFile}, extra=postExtra)


    def test_libraryTrackPost(self):
        userTest = User.objects.get(pk=USER_TEST_PK)

        token = self.test_login()
        postExtra={'HTTP_AUTHORIZATION': f'Bearer {token}'}

        currentFolder = os.path.dirname(__file__)

        imageRelativePath = settings.TEST_SAMPLE_PATH + "image.jpeg"
        tooBigSampleTrackRelativePath = (settings.TEST_SAMPLE_PATH 
            + "Big_File 1-01 - Shine On You Crazy Diamond, Parts I–V.flac")
        badExtensionSampleTrackRelativePath = settings.TEST_SAMPLE_PATH + "bad_extension.mp4"
        sampleTrackWithNonExistingGenreFooRelativePath = (
            settings.TEST_SAMPLE_PATH + "genre_foo_non_existing.mp3")
        goodFlacSampleRelativePath = settings.TEST_SAMPLE_PATH + "1-08 - Luz De Luna.flac"
        goodWavSampleRelativePath = settings.TEST_SAMPLE_PATH + "sample.wav"
        goodMp3SampleRelativePath = settings.TEST_SAMPLE_PATH + "Eminem_Without_Me_sans_genre.mp3"
        withAllTagsSampleRelativePath = settings.TEST_SAMPLE_PATH + "with_all_tags.mp3"

        imageAbsolutePath = os.path.join(currentFolder, imageRelativePath)
        tooBigSampleTrackAbsolutePath = os.path.join(currentFolder, tooBigSampleTrackRelativePath)
        badExtensionSampleTrackAbsolutePath = os.path.join(currentFolder, 
            badExtensionSampleTrackRelativePath)
        sampleTrackWithNonExistingGenreFooAbsolutePath = os.path.join(currentFolder, 
            sampleTrackWithNonExistingGenreFooRelativePath)
        goodFlacSampleAbsolutePath = os.path.join(currentFolder, goodFlacSampleRelativePath)
        goodWavSampleAbsolutePath = os.path.join(currentFolder, goodWavSampleRelativePath)
        goodMp3SampleAbsolutePath = os.path.join(currentFolder, goodMp3SampleRelativePath)
        withAllTagsSampleAbsolutePath = os.path.join(currentFolder, withAllTagsSampleRelativePath)

        response = self.postTrackFile(imageAbsolutePath, postExtra)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = self.postTrackFile(
            tooBigSampleTrackAbsolutePath, postExtra)
        print(response.content)
        # Actually the file is below the limit
        assert response.status_code == status.HTTP_201_CREATED

        response = self.postTrackFile(
            badExtensionSampleTrackAbsolutePath,
            postExtra
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = self.postTrackFile(
            sampleTrackWithNonExistingGenreFooAbsolutePath, postExtra)
        print(response.content)
        assert response.status_code == status.HTTP_201_CREATED
        assert Criteria.objects.filter(user=userTest, type__name="Foo").exists()

        response = self.postTrackFile(goodFlacSampleAbsolutePath, postExtra)
        assert response.status_code == status.HTTP_201_CREATED
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

        response = self.postTrackFile(goodWavSampleAbsolutePath, postExtra)
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

        response = self.postTrackFile(
            withAllTagsSampleAbsolutePath, postExtra)
        assert response.status_code == status.HTTP_201_CREATED

        response = self.postTrackFile(goodMp3SampleAbsolutePath, postExtra)
        assert response.status_code == status.HTTP_201_CREATED

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
