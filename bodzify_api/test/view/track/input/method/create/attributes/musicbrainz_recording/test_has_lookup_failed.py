#!/usr/bin/env python

import datetime

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_duration(self):
        response = self.post_lib_track_with_specific_sample("queen_lookup_ok.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording_lookup_has_failed_with_errors is False
