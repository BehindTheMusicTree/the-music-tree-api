#!/usr/bin/env python

import uuid

import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    @pytest.mark.critical
    def test_audio_fingerprinter_connection_ok(self):
        print("test_drown_7m21_mp3_then_ok")
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        is_reponse_ok = response.status_code == status.HTTP_201_CREATED
        if not is_reponse_ok:
            print(response.data)  # type: ignore
        assert is_reponse_ok
        file = self.lib_track_saved.track_file
        assert file
        if file.fingerprinting_error:
            print(file.fingerprinting_error)
            assert False
        else:
            assert self.lib_track_saved.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
                "4a45b00b-273d-40ed-9ecd-42f387f59c22")
