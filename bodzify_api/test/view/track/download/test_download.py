#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_ok(self):
        track_file = self.model_fixture_factory.create_file(filename="sample.mp3")
        track = self.model_fixture_factory.create_lib_track(track_file=track_file, title="We're All To Blame")
        response = self.download_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_200_OK
