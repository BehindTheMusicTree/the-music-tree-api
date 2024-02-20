#!/usr/bin/env python

from ddf import G
from rest_framework import status

from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_longest(self):
        album_artists_name = "a" * settings.ALBUM_ARTISTS_FIELD_LENGTH_MAX
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artists_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        assert list(self.saved_track.album.album_artists.all())[
            0].name == album_artists_name

    def test_when_album_artists_exist(self):
        album_artists_name = "Muse"
        artist = G(Artist, user=self.test_user, name=album_artists_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artists_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        album_artists_list = list(self.saved_track.album.album_artists.all())
        assert len(album_artists_list) == 1
        assert album_artists_list[0].uuid == artist.uuid

    def test_when_one_out_of_two_album_artists_exist(self):
        muse_artist_name = "Muse"
        muse_artist = G(Artist, user=self.test_user, name=muse_artist_name)
        bill_artist_name = "Bill"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "Starlight",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING:
            muse_artist_name + ", " + bill_artist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        muse_album_artist = self.saved_track.album.album_artists.get(
            name=muse_artist_name)
        assert muse_album_artist.uuid == muse_artist.uuid
        assert self.saved_track.album.album_artists.filter(
            name=bill_artist_name).exists()
        album_artists = list(self.saved_track.album.album_artists.all())
        assert len(album_artists) == 2

    def test_when_existing_album_with_same_album_artists(self):
        album_artists_name = "Muse"
        artist = G(Artist, user=self.test_user, name=album_artists_name)
        album_name = "Absolution"
        album = G(Album, user=self.test_user,
                  name=album_name, album_artists=[artist])
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: album_name,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: album_artists_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        assert self.saved_track.album.uuid == album.uuid
        album_artists_list = list(self.saved_track.album.album_artists.all())
        assert len(album_artists_list) == 1
        assert album_artists_list[0].uuid == artist.uuid

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

    def test_error_when_album_missing(self):
        track_url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL.URL: track_url,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_error_when_album_null(self):
        track_url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_SCHEMA_EXTRACT_ATTRIBUTES_LABEL.URL: track_url,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: None,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: "Muse",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_new_album_when_album_artists_not_provided(self):
        sum_artist = G(Artist, user=self.test_user, name="Sum 41")
        album_name = "Chuck"
        chuck_album = G(Album, user=self.test_user,
                        name=album_name, album_artists=[sum_artist])

        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: album_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        assert self.saved_track.album_id != chuck_album.uuid
        assert len(list(self.saved_track.album.album_artists.all())) == 0

    def test_sent_twice_but_should_be_created_once(self):
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

    def test_existing_album_with_same_name_but_different_album_artist(self):
        kendal_artist_name = "Kendal"
        kendal_artist = G(Artist, user=self.test_user, name=kendal_artist_name)
        album_name = "Hello"
        hello1_album = G(Album, user=self.test_user,
                         name=album_name, album_artists=[kendal_artist])
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Joie",
                  album=hello1_album,
                  duration=0)
        robertdeniro_artist = G(
            Artist, user=self.test_user, name="Robert De Niro")
        hello2_album = G(Album, user=self.test_user, name=album_name,
                         album_artists=[robertdeniro_artist])

        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: hello2_album.name,
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING: robertdeniro_artist.name,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        assert self.saved_track.album.uuid == hello2_album.uuid
        assert Album.objects.filter(
            user=self.test_user, name=album_name).count() == 1
        assert Artist.objects.filter(
            user=self.test_user, name=kendal_artist_name).exists() == False

    def test_one_existing_album_artist_and_one_not(self):
        pnl_artist = G(Artist, user=self.test_user, name="PNL")
        triste_artist_name = "Triste"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Joie",
                  duration=0)

        data = {
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_NAME: "VOLART",
            TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAMES_STRING:
            pnl_artist.name + "," + triste_artist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        album_artists_list = list(self.saved_track.album.album_artists.all())
        assert len(album_artists_list) == 2
        assert pnl_artist in album_artists_list
        triste_artist = Artist.objects.get(
            user=self.test_user, name=triste_artist_name)
        assert triste_artist in album_artists_list
