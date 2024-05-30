#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_totaleclipe_5m35_with_three_scores_then_highest(self):
        response = self.post_lib_track_with_specific_sample("total_eclipse_three_scores.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert float(self.saved_lib_track.musicbrainz_recording.score) == 0.98117745  # type: ignore
