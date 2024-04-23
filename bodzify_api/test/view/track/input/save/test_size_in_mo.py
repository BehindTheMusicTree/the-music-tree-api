#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
import math


class TestCase(TrackTestCase):

    def test_wav(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        size_in_mo = self.saved_lib_track.file_obj.size / (1024 * 1024)
        assert math.isclose(size_in_mo, self.LIB_TRACK_GENERIC_SAMPLES_TAGS_NONE_SIZE_IN_MO.WAV, rel_tol=0.1)

    def test_mp3(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        size_in_mo = self.saved_lib_track.file_obj.size / (1024 * 1024)
        assert math.isclose(size_in_mo, self.LIB_TRACK_GENERIC_SAMPLES_TAGS_NONE_SIZE_IN_MO.MP3, rel_tol=0.1)

    def test_flac(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension='flac')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        size_in_mo = self.saved_lib_track.file_obj.size / (1024 * 1024)
        assert math.isclose(size_in_mo, self.LIB_TRACK_GENERIC_SAMPLES_TAGS_NONE_SIZE_IN_MO.FLAC, rel_tol=0.1)
