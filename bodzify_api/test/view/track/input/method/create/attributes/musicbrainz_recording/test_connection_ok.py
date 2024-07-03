#!/usr/bin/env python

import uuid
import pytest

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    @pytest.mark.critical
    def test_drown_7m21_mp3_then_ok(self):
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
            assert False
        else:
            assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
                "4a45b00b-273d-40ed-9ecd-42f387f59c22")
