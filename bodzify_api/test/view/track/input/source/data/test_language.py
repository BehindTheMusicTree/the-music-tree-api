#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import \
    FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.input.source.data.LibTrackAttributeFromDataTestCase import \
    LibTrackAttributeFromDataTestCase


class TestCase(LibTrackAttributeFromDataTestCase):

    def test_not_empty_then_ok(self):
        language = "a"
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            PUT_FIELDS.LANGUAGE: language
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == language

    def test_empty_then_ok(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      language="French",
                      duration=0)
        data = {
            PUT_FIELDS.LANGUAGE: ""
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

    def test_null_then_ok(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      language="French",
                      duration=0)
        data = {
            PUT_FIELDS.LANGUAGE: None
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
