#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.input.method.put.AttributePutTestCase import AttributeFromPutTestCase


class TestCase(AttributeFromPutTestCase):

    def test_not_empty_then_ok(self):
        title = "a"
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            PUT_FIELDS.TITLE: title
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.title == title

    def test_not_provided_then_unchanged(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      duration=0)
        data = {}
        response = self.put_lib_track(lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.title == None

    def test_none_then_none(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            PUT_FIELDS.TITLE: None
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.title == None

    def test_empty_then_none(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            PUT_FIELDS.TITLE: ""
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.title == None

    def test_not_none_then_update(self):
        title = "a"
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title=title,
                      duration=0)
        data = {
            PUT_FIELDS.TITLE: title
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.title == title
