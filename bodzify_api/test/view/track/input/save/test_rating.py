#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_zero(self):
        rating = 0
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      duration=0)
        data = {
            "rating": rating
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
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
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
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
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.rating == rating

    def test_error_when_above_maximum(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": 11,
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_error_when_below_minimum(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": -1,
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_error_when_not_integer(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Korinto",
                      rating=3,
                      duration=0)
        data = {
            "rating": 5.5,
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
