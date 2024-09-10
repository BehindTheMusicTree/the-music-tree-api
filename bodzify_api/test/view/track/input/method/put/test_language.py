#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.endpoint.put import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.input.method.put.NullableFieldTestCase import NullableFieldTestCase


class TestCase(NullableFieldTestCase):

    def test_not_empty_then_ok(self):
        language = "a"
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PUT_FIELDS.LANGUAGE: language}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == language

    def test_not_provided_then_unchanged(self):
        language = "French"
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", language=language)
        response = self.put_lib_track(lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == language

    def test_empty_then_none(self):
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", language="French")
        data = {PUT_FIELDS.LANGUAGE: ""}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == None

    def test_not_none_then_update(self):
        language = "a"
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", language="French")
        data = {PUT_FIELDS.LANGUAGE: language}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == language
