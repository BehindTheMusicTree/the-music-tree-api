import os

from django.urls import reverse
from django.test import TestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames

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


    def test_libraryTrackPost(self):
        userTest = User.objects.get(pk=USER_TEST_PK)
        client = Client()

        script_dir = os.path.dirname(__file__)
        rel_path = "sample/Eminem_Without_Me.mp3"
        abs_file_path = os.path.join(script_dir, rel_path)
        print(abs_file_path)
        with open(abs_file_path) as file:
            response = client.post('/tracks/', {'track': file})
        assert response.status_code == 201

        track = LibraryTrack.objects.get(__path__endswith="Eminem_Without_Me.mp3", user=userTest)
        assert track.title == "Without Me"
        assert track.artist == "Eminem"
        assert track.album == "The Eminem Show (Expanded Edition)"
        assert track.genre == "US Rap"
        assert track.fileExtension == ".mp3"

        assert Playlist.objects.get(
            user=userTest,
            name=PlaylistSpecialNames.GENRE_ALL
        ) in track.playlists

        assert Playlist.objects.get(
            user=userTest,
            name=PlaylistSpecialNames.GENRE_GENRELESS
        ) in track.playlists

        assert Playlist.objects.get(
            user=userTest,
            name="US Rap"
        ) in track.playlists

        assert Playlist.objects.get(
            user=userTest,
            name=PlaylistSpecialNames.TAG_ALL
        ) in track.playlists
