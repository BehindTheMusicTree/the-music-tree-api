#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.NotNullableFieldTestCase import \
    NotNullableFieldTestCase


class TestCase(NotNullableFieldTestCase):

    def test_not_empty_then_ok(self):
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")
        title_new = "a"
        data = {PutFields.TITLE: title_new}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.title == title_new

    def test_not_provided_then_unchanged(self):
        old_title = "Love"
        lib_track = self.model_fixture_factory.create_lib_track(title=old_title)
        response = self.put_lib_track(lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.title == old_title

    def test_empty_then_error(self):
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.TITLE: ""}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_none_then_update(self):
        title = "a"
        lib_track = self.model_fixture_factory.create_lib_track(title=title)
        data = {PutFields.TITLE: title}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.title == title
