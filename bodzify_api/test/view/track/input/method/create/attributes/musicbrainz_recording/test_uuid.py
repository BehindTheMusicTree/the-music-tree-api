#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
import bodzify_api.audiometadata as audiometadata


class TestCase(TrackTestCase):

    def test_drown_7m21(self):
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == "d2fe3873-d123-4bea-a5ee-4340d865777c"  # type: ignore
