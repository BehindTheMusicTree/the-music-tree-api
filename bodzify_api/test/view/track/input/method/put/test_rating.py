#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_not_provided_then_unchanged(self):
        rating = 5
        lib_track = self.model_fixture_factory.create_lib_track(title="Korinto", rating=rating)
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating

    def test_zero(self):
        rating = 0
        lib_track = self.model_fixture_factory.create_lib_track(title="Korinto")
        data = {PUT_FIELDS.RATING: rating}
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating
