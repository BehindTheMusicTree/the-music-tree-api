#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_longest(self):
        albumArtistsName = "a" * settings.ALBUM_ARTISTS_FIELD_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        assert list(self.saved_track.album.albumArtists.all())[
            0].name == albumArtistsName

    def test_whenAlbumArtistsExist(self):
        albumArtistsName = "Muse"
        artist = G(Artist, user=self.test_user, name=albumArtistsName)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        albumArtistsList = list(self.saved_track.album.albumArtists.all())
        assert len(albumArtistsList) == 1
        assert albumArtistsList[0].uuid == artist.uuid

    def test_whenOneOutOfTwoAlbumArtistsExist(self):
        museArtistName = "Muse"
        museArtist = G(Artist, user=self.test_user, name=museArtistName)
        billArtistName = "Bill"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Starlight",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: \
                museArtistName + ", " + billArtistName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        museAlbumArtist = self.saved_track.album.albumArtists.get(
            name=museArtistName)
        assert museAlbumArtist.uuid == museArtist.uuid
        assert self.saved_track.album.albumArtists.filter(
            name=billArtistName).exists()
        albumArtists = list(self.saved_track.album.albumArtists.all())
        assert len(albumArtists) == 2

    def test_whenExistingAlbumWithSameAlbumArtists(self):
        albumArtistsName = "Muse"
        artist = G(Artist, user=self.test_user, name=albumArtistsName)
        albumName = "Absolution"
        album = G(Album, user=self.test_user,
                  name=albumName, albumArtists=[artist])
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: albumName,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.saved_track.album.uuid == album.uuid
        albumArtistsList = list(self.saved_track.album.albumArtists.all())
        assert len(albumArtistsList) == 1
        assert albumArtistsList[0].uuid == artist.uuid

    def test_nullThenNone(self):        
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: None
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert len(list(self.saved_track.album.albumArtists.all())) == 0

    def test_emptyThenNone(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: ""
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert len(list(self.saved_track.album.albumArtists.all())) == 0

    def test_errorWhenAlbumMissing(self):
        trackUrl = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL.URL: trackUrl,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenAlbumNull(self):
        trackUrl = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL.URL: trackUrl,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: None,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_newAlbumWhenAlbumArtistsNotProvided(self):
        sumArtist = G(Artist, user=self.test_user, name="Sum 41")
        albumName = "Chuck"
        chuckAlbum = G(Album, user=self.test_user,
                       name=albumName, albumArtists=[sumArtist])
        
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: albumName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.saved_track.album_id != chuckAlbum.uuid
        assert len(list(self.saved_track.album.albumArtists.all())) == 0

    def test_sentTwiceButShouldBeCreatedOnce(self):
        artistName = "Sum"
        albumName = "Chuck"
        
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: albumName,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: artistName + "," + artistName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert Album.objects.get(
            user=self.test_user, name=albumName).albumArtists.count() == 1
        assert Artist.objects.filter(
            user=self.test_user, name=artistName).count() == 1

    def test_existingAlbumWithSameNameButDifferentAlbumArtist(self):
        kendalArtistName = "Kendal"
        kendalArtist = G(Artist, user=self.test_user, name=kendalArtistName)
        albumName = "Hello"
        hello1Album = G(Album, user=self.test_user,
                        name=albumName, albumArtists=[kendalArtist])
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Joie",
                  album=hello1Album,
                  duration=0)
        robertdeniroArtist = G(
            Artist, user=self.test_user, name="Robert De Niro")
        hello2Album = G(Album, user=self.test_user, name=albumName,
                        albumArtists=[robertdeniroArtist])
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: hello2Album.name,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: robertdeniroArtist.name,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.saved_track.album.uuid == hello2Album.uuid
        assert Album.objects.filter(
            user=self.test_user, name=albumName).count() == 1
        assert Artist.objects.filter(
            user=self.test_user, name=kendalArtistName).exists() == False

    def test_oneExistingAlbumArtistAndOneNot(self):
        pnlArtist = G(Artist, user=self.test_user, name="PNL")
        tristeArtistName = "Triste"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Joie",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "VOLART",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: \
                pnlArtist.name + "," + tristeArtistName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        albumArtistsList = list(self.saved_track.album.albumArtists.all())
        assert len(albumArtistsList) == 2
        assert pnlArtist in albumArtistsList
        tristeArtist = Artist.objects.get(
            user=self.test_user, name=tristeArtistName)
        assert tristeArtist in albumArtistsList
