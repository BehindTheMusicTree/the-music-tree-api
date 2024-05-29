#!/usr/bin/env python

import uuid

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
import bodzify_api.audiometadata as audiometadata


class TestCase(TrackTestCase):

    def test_drown_7m21(self):
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(
            "4a45b00b-273d-40ed-9ecd-42f387f59c22")  # type: ignore
