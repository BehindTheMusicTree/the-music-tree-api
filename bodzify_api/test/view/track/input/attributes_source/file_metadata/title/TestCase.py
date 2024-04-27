#!/usr/bin/env python

import logging
from bodzify_api import settings
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):
    file_extension: str

    def test_none_then_ok_because_generated(self):
        response = self.post_lib_track_with_generic_sample_no_tags(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title is not None

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.title == 'a' * settings.ALBUM_NAME_LENGTH_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
