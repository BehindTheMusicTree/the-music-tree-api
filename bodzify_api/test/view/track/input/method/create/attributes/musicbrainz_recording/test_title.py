#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_drown_7m21_mp3_then_ok(self):
        response = self.post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.title == "Drown (Massano remix)"  # type: ignore

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self.post_lib_track_with_specific_sample("Bonnie Tyler - Total Eclipse of the Heart - 5m35.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.title == "Total Eclipse of the Heart"  # type: ignore
