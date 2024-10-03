#!/usr/bin/env python

import datetime

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_multiple_release_dates_then_earliest(self):
        response = self.post_lib_track_with_specific_sample("queen_multiple_release_dates.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.musicbrainz_recording.release_date == datetime.date(1977, 10, 28)  # type: ignore
