#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.track.input.source.data.LibTrackAttributeFromDataTestCase import \
    LibTrackAttributeFromDataTestCase


class TestCase(LibTrackAttributeFromDataTestCase):

    def test_not_empty_then_ok(self):
        artist_name = 'a'
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: artist_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_then_ok(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: ""
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

    def test_null_then_ok(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: None
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
