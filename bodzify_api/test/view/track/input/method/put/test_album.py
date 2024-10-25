#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.serializer.schema.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.NullableFieldTestCase import \
    NullableFieldTestCase


class TestCase(NullableFieldTestCase):

    def test_not_provided_then_unchanged(self):
        album = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", album=album)
        response = self._put_lib_track(lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.album == album

    def test_empty_then_none(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        data = {PutFields.ALBUM_NAME: ''}
        response = self._put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.album == None

    def test_not_none_then_update(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        album_new = self.model_fixture_factory.create_album(name="koko")
        data = {PutFields.ALBUM_NAME: album_new.name}
        response = self._put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.album == album_new

    def test_nothing_linked_to_old_album_anymore_then_delete(self):
        album_name = "Le Noir"
        album = self.model_fixture_factory.create_album(name=album_name)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)
        data = {PutFields.ALBUM_NAME: "Paul"}
        response = self._put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert not Album.objects.filter(user=self.test_user1, name=album_name).exists()

    def test_a_track_still_linked_to_album_then_not_delete(self):
        album_name = "La Saucisse"
        album = self.model_fixture_factory.create_album(name=album_name)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Foire", album=album)
        self.model_fixture_factory.create_lib_track_with_file(title="Josie", album=album)
        data = {PutFields.ALBUM_NAME: "Paul"}
        response = self._put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(user=self.test_user1, name=album_name).exists()
