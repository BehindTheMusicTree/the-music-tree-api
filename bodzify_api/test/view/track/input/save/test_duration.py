#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.ApiTestCase import ApiTestCase


class TestCase(ApiTestCase):

    def test_wav(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.duration == self.SAMPLE_LIB_TRACK_WAV_DURATION  # type: ignore

    def test_mp3(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.duration == self.SAMPLE_LIB_TRACK_MP3_DURATION  # type: ignore

    def test_flac(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension='flac')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.duration == self.SAMPLE_LIB_TRACK_FLAC_DURATION  # type: ignore
