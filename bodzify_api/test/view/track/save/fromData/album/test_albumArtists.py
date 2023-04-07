#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class AlbumArtistsTestCase(TrackViewTestCase):

    def test_longest(self):
        albumArtistsName = "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": "Chuck",
            "albumArtistsName": albumArtistsName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert list(self.savedTrack.album.albumArtists.all())[
            0].name == albumArtistsName

    def test_whenAlbumArtistsExist(self):
        albumArtistsName = "Muse"
        artist = G(Artist, user=self.testUser, name=albumArtistsName)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": "Starlight",
            "albumArtistsName": albumArtistsName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsList = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtistsList) == 1
        assert albumArtistsList[0].uuid == artist.uuid

    def test_whenOneOutOfTwoAlbumArtistsExist(self):
        museArtistName = "Muse"
        museArtist = G(Artist, user=self.testUser, name=museArtistName)
        billArtistName = "Bill"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": "Starlight",
            "albumArtistsName": museArtistName + ", " + billArtistName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        museAlbumArtist = self.savedTrack.album.albumArtists.get(
            name=museArtistName)
        assert museAlbumArtist.uuid == museArtist.uuid
        assert self.savedTrack.album.albumArtists.filter(
            name=billArtistName).exists()
        albumArtists = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtists) == 2

    def test_whenExistingAlbumWithSameAlbumArtists(self):
        albumArtistsName = "Muse"
        artist = G(Artist, user=self.testUser, name=albumArtistsName)
        albumName = "Absolution"
        album = G(Album, user=self.testUser,
                  name=albumName, albumArtists=[artist])
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName,
            "albumArtistsName": albumArtistsName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.uuid == album.uuid
        albumArtistsList = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtistsList) == 1
        assert albumArtistsList[0].uuid == artist.uuid

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": "Chuck",
            "albumArtistsName": None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0

    def test_empty(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": "Chuck",
            "albumArtistsName": ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0

    def test_errorWhenAlbumMissing(self):
        trackUrl = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            "url": trackUrl,
            "albumArtistsName": "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenAlbumNull(self):
        trackUrl = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            "url": trackUrl,
            "albumName": None,
            "albumArtistsName": "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_newAlbumWhenAlbumArtistsNotSpecified(self):
        sumArtist = G(Artist, user=self.testUser, name="Sum 41")
        albumName = "Chuck"
        chuckAlbum = G(Album, user=self.testUser,
                       name=albumName, albumArtists=[sumArtist])
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album_id != chuckAlbum.uuid
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0

    def test_sentTwiceButShouldBeCreatedOnce(self):
        artistName = "Sum"
        albumName = "CHuck"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName,
            "albumArtistsName": artistName + "," + artistName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Album.objects.get(
            user=self.testUser, name=albumName).albumArtists.count() == 1
        assert Artist.objects.filter(
            user=self.testUser, name=artistName).count() == 1

    def test_existingAlbumWithSameNameButDifferentAlbumArtist(self):
        kendalArtistName = "Kendal"
        kendalArtist = G(Artist, user=self.testUser, name=kendalArtistName)
        albumName = "Hello"
        hello1Album = G(Album, user=self.testUser,
                        name=albumName, albumArtists=[kendalArtist])
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Joie",
                  album=hello1Album,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        robertdeniroArtist = G(
            Artist, user=self.testUser, name="Robert De Niro")
        hello2Album = G(Album, user=self.testUser, name=albumName,
                        albumArtists=[robertdeniroArtist])
        data = {
            "albumName": hello2Album.name,
            "albumArtistsName": robertdeniroArtist.name,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.uuid == hello2Album.uuid
        assert Album.objects.filter(
            user=self.testUser, name=albumName).count() == 1
        assert Artist.objects.filter(
            user=self.testUser, name=kendalArtistName).exists() == False

    def test_oneExistingAlbumArtistAndOneNot(self):
        pnlArtist = G(Artist, user=self.testUser, name="PNL")
        tristeArtistName = "Triste"
        response = self.postSampleTrack("oneExistingAlbumArtistAndOneNot.flac")
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsList = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtistsList) == 2
        assert pnlArtist in albumArtistsList
        tristeArtist = Artist.objects.get(user=self.testUser, name=tristeArtistName)
        assert tristeArtist in albumArtistsList
