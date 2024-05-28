#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
import bodzify_api.audiometadata as audiometadata


class TestCase(TrackTestCase):

    def test_totaleclipse_3m31(self):
        response = self.post_lib_track_with_specific_sample("Bonnie Tyler - Total Eclipse of the Heart - 3m31.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording_id == "f3b3b0f4-2cfb-4d0a-853e-2a3b2b7e6d4b"
