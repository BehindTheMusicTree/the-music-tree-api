#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.serializer.track.input.schema.LibTrackPutSerializer import FIELDS as PUT_FIELDS


class TestCase(ApiTestCase):

    def test_not_provided_then_unchanged(self):
        rating = 5
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=rating,
                      duration=0)
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict={})  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.rating == rating

    def test_zero(self):
        rating = 0
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      duration=0)
        data = {
            PUT_FIELDS.RATING: rating
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.rating == rating
