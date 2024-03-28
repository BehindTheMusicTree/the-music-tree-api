#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.input.method.put.NullableFieldTestCase import NullableFieldTestCase


class TestCase(NullableFieldTestCase):

    def test_not_provided_then_unchanged(self):
        album = G(Album, user=self.test_user, name="Jojo")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      album=album,
                      duration=0)
        response = self.put_lib_track(lib_track.uuid, data_dict={})  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.album == album

    def test_empty_then_none(self):
        album_old = G(Album, user=self.test_user, name="Jojo")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      album=album_old,
                      duration=0)
        data = {
            PUT_FIELDS.ALBUM_NAME: ''
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.album == None

    def test_not_none_then_update(self):
        album_old = G(Album, user=self.test_user, name="Jojo")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      album=album_old,
                      duration=0)
        album_new = G(Album, user=self.test_user, name="koko")
        data = {
            PUT_FIELDS.ALBUM_NAME: album_new.name  # type: ignore
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.album == album_new

    def test_nothing_linked_to_old_album_anymore_then_delete(self):
        album_name = "Le Noir"
        album = G(Album, user=self.test_user, name=album_name)
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Foire",
                      album=album,
                      duration=0)
        data = {
            PUT_FIELDS.ALBUM_NAME: "Paul",
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert not Album.objects.filter(user=self.test_user, name=album_name).exists()

    def test_a_track_still_linked_to_album_then_not_delete(self):
        album_name = "La Saucisse"
        album = G(Album, user=self.test_user, name=album_name)
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Foire",
                      album=album,
                      duration=0)
        G(LibraryTrack,
          user=self.test_user,
          title="Josie",
          album=album,
          duration=0)
        data = {
            PUT_FIELDS.ALBUM_NAME: "Paul",
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert Album.objects.filter(user=self.test_user, name=album_name).exists()
