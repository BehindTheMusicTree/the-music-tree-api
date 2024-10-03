#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_totaleclipse_with_three_scores_then_highest(self):
        response = self.post_lib_track_with_specific_sample("total_eclipse_3_scores.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert float(self.lib_track_saved.musicbrainz_recording.score) > 0.98  # type: ignore
