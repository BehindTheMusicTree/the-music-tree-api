#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.NullableFieldTestCase import NullableFieldTestCase


class TestCase(NullableFieldTestCase):

    def test_not_provided_then_unchanged(self):
        artist = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", artist=artist)
        response = self.put_lib_track(lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.artist == artist

    def test_empty_then_none(self):
        artist_old = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track(title="koko", artist=artist_old)
        data = {PutFields.ARTIST_NAME: ''}
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.artist == None

    def test_not_none_then_update(self):
        artist_old = self.model_fixture_factory.create_artist(name="a-ha")
        lib_track = self.model_fixture_factory.create_lib_track(title="koko", artist=artist_old)
        artist_new = self.model_fixture_factory.create_artist(name="Koko")
        data = {PutFields.ARTIST_NAME: artist_new.name}
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.artist == artist_new

    def test_delete_old_one_because_nothing_linked_to_it(self):
        artist_name = "a-ha"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track(title="Foire", artist=artist)
        data = {PutFields.ARTIST_NAME: "Autre artiste"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert not Artist.objects.filter(name=artist_name).exists()

    def test_not_delete_old_one_because_a_track_linked_to_it(self):
        artist_name = "a-ha"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track(title="Foire", artist=artist)
        self.model_fixture_factory.create_lib_track(title="Josie", artist=artist)
        data = {PutFields.ARTIST_NAME: artist_name}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(name=artist_name).exists()

    def test_not_delete_old_one_because_an_album_linked_to_it(self):
        artist_name = "a-ha"
        artist = self.model_fixture_factory.create_artist(name=artist_name)
        track = self.model_fixture_factory.create_lib_track(title="Foire", artist=artist)
        album = self.model_fixture_factory.create_album(name="Hunting High and Low", album_artists=[artist])
        self.model_fixture_factory.create_lib_track(title="Josie", album=album)
        data = {PutFields.ARTIST_NAME: artist_name}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(name=artist_name).exists()
