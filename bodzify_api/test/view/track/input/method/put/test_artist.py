#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.input.method.put.FieldTestCase import FieldTestCase


class TestCase(FieldTestCase):

    def test_not_provided_then_unchanged(self):
        artist = G(Artist, user=self.test_user, name="a-ha")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      artist=artist,
                      duration=0)
        response = self.put_lib_track(lib_track.uuid, data_dict={})  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.artist == artist

    def test_empty_then_none(self):
        artist_old = G(Artist, user=self.test_user, name="a-ha")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      artist=artist_old,
                      duration=0)
        data = {
            PUT_FIELDS.ARTIST_NAME: ''
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.artist == None

    def test_not_none_then_update(self):
        artist_old = G(Artist, user=self.test_user, name="a-ha")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      artist=artist_old,
                      duration=0)
        artist_new = G(Artist, user=self.test_user, name="Koko")
        data = {
            PUT_FIELDS.ARTIST_NAME: artist_new.name  # type: ignore
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.artist == artist_new

    def test_delete_old_one_because_nothing_linked_to_it(self):
        artist_name = "a-ha"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  artist=artist,
                  duration=0)
        data = {
            PUT_FIELDS.ARTIST_NAME: "Autre artiste"
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert not Artist.objects.filter(user=self.test_user, name=artist_name).exists()

    def test_not_delete_old_one_because_a_track_linked_to_it(self):
        artist_name = "a-ha"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  artist=artist,
                  duration=0)
        G(LibraryTrack,
          user=self.test_user,
          title="Josie",
          artist=artist,
          duration=0)
        data = {
            PUT_FIELDS.ARTIST_NAME: artist_name
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert Artist.objects.filter(user=self.test_user, name=artist_name).exists()

    def test_not_delete_old_one_because_an_album_linked_to_it(self):
        artist_name = "a-ha"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  artist=artist,
                  duration=0)
        album = G(Album, user=self.test_user, name="Hunting High and Low", album_artists=[artist])
        G(LibraryTrack,
          user=self.test_user,
          title="Josie",
          album=album,
          duration=0)
        data = {
            PUT_FIELDS.ARTIST_NAME: artist_name
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert Artist.objects.filter(user=self.test_user, name=artist_name).exists()
