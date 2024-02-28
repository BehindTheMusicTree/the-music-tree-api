#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import \
    FIELDS as PUT_FIELDS


class TestCase(ApiViewTestCase):

    def test_not_provided_then_unchanged(self):
        rating = 5
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=rating,
                      duration=0)
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating

    def test_zero(self):
        rating = 0
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      duration=0)
        data = {
            "rating": rating
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating

    def test_four(self):
        rating = 4
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      duration=0)
        data = {
            "rating": rating
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating

    def test_ten(self):
        rating = 10
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      duration=0)
        data = {
            "rating": rating
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating

    def test_none(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": None
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == None

    def test_errorWhenAboveMaximum(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": 11,
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenBelowMinimum(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": -1,
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenNotInteger(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": 5.5,
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
