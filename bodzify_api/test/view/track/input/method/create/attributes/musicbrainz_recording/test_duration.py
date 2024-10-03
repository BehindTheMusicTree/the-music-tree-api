#!/usr/bin/env python

import datetime

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_duration_greater_to_one_sec_then_ok(self):
        response = self.post_lib_track_with_specific_sample("queen_duration_181.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.musicbrainz_recording.duration_in_sec == 181  # type: ignore

    def test_duration_lesser_than_one_sec_then_no_recording(self):
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.musicbrainz_recording is None
        assert self.lib_track_saved.musicbrainz_recording_lookup_error_str is None
