#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenUnchanged(self):
        rating = 5
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  rating=rating,
                  duration=0)
        data = {}
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == rating

    def test_zero(self):
        rating = 0
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  duration=0)
        data = {
            "rating": rating
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == rating

    def test_four(self):
        rating = 4
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  duration=0)
        data = {
            "rating": rating
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == rating

    def test_ten(self):
        rating = 10
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  duration=0)
        data = {
            "rating": rating
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == rating

    def test_none(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  rating=3,
                  duration=0)
        data = {
            "rating": None
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.rating == None

    def test_errorWhenAboveMaximum(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  rating=3,
                  duration=0)
        data = {
            "rating": 11,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenBelowMinimum(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  rating=3,
                  duration=0)
        data = {
            "rating": -1,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_errorWhenNotInteger(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Korinto",
                  rating=3,
                  duration=0)
        data = {
            "rating": 5.5,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
