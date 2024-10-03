#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.Album import Album
from bodzify_api.serializer.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.test.view.track.input.attributes_source import data
from bodzify_api.test.view.track.input.method.put.NullableFieldTestCase import NullableFieldTestCase


class TestCase(TrackTestCase):

    def test_not_provided_then_unchanged_false(self):
        track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.TITLE: "Love"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.archived == False

    def test_not_provided_then_unchanged_true(self):
        track = self.model_fixture_factory.create_lib_track(title="Love", archived=True)
        data = {PutFields.TITLE: "Love"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.archived == True

    def test_empty_then_error(self):
        track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.ARCHIVED: ''}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_boolean_then_error(self):
        track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.ARCHIVED: 'koko'}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_true_then_update(self):
        track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.ARCHIVED: "true"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.archived == True

    def test_true_in_capital_letters_then_update(self):
        track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.ARCHIVED: 'TRUE'}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.archived == True

    def test_false_then_update(self):
        track = self.model_fixture_factory.create_lib_track(title="Love", archived=True)
        data = {PutFields.ARCHIVED: "false"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.archived == False

    def test_false_in_capital_letters_then_update(self):
        track = self.model_fixture_factory.create_lib_track(title="Love", archived=True)
        data = {PutFields.ARCHIVED: 'FALSE'}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.archived == False
