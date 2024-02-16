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
        album_artistsName = "a" * settings.ALBUM_ARTISTS_FIELD_LENGTH_MAX
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artistsName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        assert list(self.saved_track.album.album_artists.all())[
            0].name == album_artistsName

    def test_whenalbum_artistsExist(self):
        album_artistsName = "Muse"
        artist = G(Artist, user=self.test_user, name=album_artistsName)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artistsName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        album_artistsList = list(self.saved_track.album.album_artists.all())
        assert len(album_artistsList) == 1
        assert album_artistsList[0].uuid == artist.uuid

    def test_whenOneOutOfTwoalbum_artistsExist(self):
        museartist_name = "Muse"
        museArtist = G(Artist, user=self.test_user, name=museartist_name)
        billartist_name = "Bill"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Starlight",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: \
                museartist_name + ", " + billartist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        museAlbumArtist = self.saved_track.album.album_artists.get(
            name=museartist_name)
        assert museAlbumArtist.uuid == museArtist.uuid
        assert self.saved_track.album.album_artists.filter(
            name=billartist_name).exists()
        album_artists = list(self.saved_track.album.album_artists.all())
        assert len(album_artists) == 2

    def test_whenExistingAlbumWithSamealbum_artists(self):
        album_artistsName = "Muse"
        artist = G(Artist, user=self.test_user, name=album_artistsName)
        album_name = "Absolution"
        album = G(Album, user=self.test_user,
                  name=album_name, album_artists=[artist])
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: album_name,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artistsName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.saved_track.album.uuid == album.uuid
        album_artistsList = list(self.saved_track.album.album_artists.all())
        assert len(album_artistsList) == 1
        assert album_artistsList[0].uuid == artist.uuid

    def test_null_then_none(self):        
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: None
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert len(list(self.saved_track.album.album_artists.all())) == 0

    def test_empty_then_none(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: ""
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert len(list(self.saved_track.album.album_artists.all())) == 0

    def test_errorWhenAlbumMissing(self):
        track_url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL.URL: track_url,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenAlbumNull(self):
        track_url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL.URL: track_url,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: None,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_newAlbumWhenalbum_artistsNotProvided(self):
        sumArtist = G(Artist, user=self.test_user, name="Sum 41")
        album_name = "Chuck"
        chuckAlbum = G(Album, user=self.test_user,
                       name=album_name, album_artists=[sumArtist])
        
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: album_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.saved_track.album_id != chuckAlbum.uuid
        assert len(list(self.saved_track.album.album_artists.all())) == 0

    def test_sentTwiceButShouldBeCreatedOnce(self):
        artist_name = "Sum"
        album_name = "Chuck"
        
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: album_name,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: artist_name + "," + artist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert Album.objects.get(
            user=self.test_user, name=album_name).album_artists.count() == 1
        assert Artist.objects.filter(
            user=self.test_user, name=artist_name).count() == 1

    def test_existingAlbumWithSameNameButDifferentAlbumArtist(self):
        kendalartist_name = "Kendal"
        kendalArtist = G(Artist, user=self.test_user, name=kendalartist_name)
        album_name = "Hello"
        hello1Album = G(Album, user=self.test_user,
                        name=album_name, album_artists=[kendalArtist])
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Joie",
                  album=hello1Album,
                  duration=0)
        robertdeniroArtist = G(
            Artist, user=self.test_user, name="Robert De Niro")
        hello2Album = G(Album, user=self.test_user, name=album_name,
                        album_artists=[robertdeniroArtist])
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: hello2Album.name,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: robertdeniroArtist.name,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        assert self.saved_track.album.uuid == hello2Album.uuid
        assert Album.objects.filter(
            user=self.test_user, name=album_name).count() == 1
        assert Artist.objects.filter(
            user=self.test_user, name=kendalartist_name).exists() == False

    def test_oneExistingAlbumArtistAndOneNot(self):
        pnlArtist = G(Artist, user=self.test_user, name="PNL")
        tristeartist_name = "Triste"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Joie",
                  duration=0)
        
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "VOLART",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: \
                pnlArtist.name + "," + tristeartist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        
        album_artistsList = list(self.saved_track.album.album_artists.all())
        assert len(album_artistsList) == 2
        assert pnlArtist in album_artistsList
        tristeArtist = Artist.objects.get(
            user=self.test_user, name=tristeartist_name)
        assert tristeArtist in album_artistsList
