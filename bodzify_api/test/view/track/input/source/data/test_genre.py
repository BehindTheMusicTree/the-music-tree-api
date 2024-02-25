#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.LibTrackSchemaPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.test.view.track.input.source.data.LibTrackAttributeFromDataTestCase import \
    LibTrackAttributeFromDataTestCase


class TestCase(LibTrackAttributeFromDataTestCase):

    def test_not_empty_then_ok(self):
        genre_name = "a"
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      duration=0)
        data = {
            PUT_FIELDS.GENRE_NAME: genre_name
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

    def test_empty_then_ok(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      genre=self.saved_genre,
                      duration=0)
        data = {
            PUT_FIELDS.GENRE_NAME: ""
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

    def test_null_then_ok(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      genre=self.saved_genre,
                      duration=0)
        data = {
            PUT_FIELDS.GENRE_NAME: None
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
