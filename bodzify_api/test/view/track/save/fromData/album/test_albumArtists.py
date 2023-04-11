#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class AlbumArtistsTestCase(ApiViewTestCase):

    def test_longest(self):
        albumArtistsName = "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK

        assert list(self.savedTrack.album.albumArtists.all())[
            0].name == albumArtistsName

    def test_whenAlbumArtistsExist(self):
        albumArtistsName = "Muse"
        artist = G(Artist, user=self.testUser, name=albumArtistsName)
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK

        albumArtistsList = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtistsList) == 1
        assert albumArtistsList[0].uuid == artist.uuid

    def test_whenOneOutOfTwoAlbumArtistsExist(self):
        museArtistName = "Muse"
        museArtist = G(Artist, user=self.testUser, name=museArtistName)
        billArtistName = "Bill"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Starlight",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: \
                museArtistName + ", " + billArtistName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK

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
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: albumName,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.savedTrack.album.uuid == album.uuid
        albumArtistsList = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtistsList) == 1
        assert albumArtistsList[0].uuid == artist.uuid

    def test_nullThenNone(self):        
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: None
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0

    def test_emptyThenNone(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: ""
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
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

    def test_newAlbumWhenAlbumArtistsNotProvided(self):
        sumArtist = G(Artist, user=self.testUser, name="Sum 41")
        albumName = "Chuck"
        chuckAlbum = G(Album, user=self.testUser,
                       name=albumName, albumArtists=[sumArtist])
        
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: albumName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.savedTrack.album_id != chuckAlbum.uuid
        assert len(list(self.savedTrack.album.albumArtists.all())) == 0

    def test_sentTwiceButShouldBeCreatedOnce(self):
        artistName = "Sum"
        albumName = "Chuck"
        
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: albumName,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: artistName + "," + artistName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
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
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Joie",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "VOLART",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: \
                pnlArtist.name + "," + tristeArtistName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.status_code == status.HTTP_201_CREATED
        
        albumArtistsList = list(self.savedTrack.album.albumArtists.all())
        assert len(albumArtistsList) == 2
        assert pnlArtist in albumArtistsList
        tristeArtist = Artist.objects.get(
            user=self.testUser, name=tristeArtistName)
        assert tristeArtist in albumArtistsList
